package com.sports.modules.result.service.impl;

import com.alibaba.excel.EasyExcel;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.sports.common.exception.BusinessException;
import com.sports.common.result.ResultCode;
import com.sports.modules.event.entity.Event;
import com.sports.modules.event.service.EventService;
import com.sports.modules.result.dto.ResultImportRow;
import com.sports.modules.result.entity.CompetitionResult;
import com.sports.modules.result.mapper.CompetitionResultMapper;
import com.sports.modules.result.service.CompetitionResultService;
import com.sports.modules.result.vo.CompetitionResultVO;
import com.sports.modules.sportitem.entity.SportItem;
import com.sports.modules.sportitem.service.SportItemService;
import com.sports.modules.system.entity.SysUser;
import com.sports.modules.system.service.SysUserService;
import com.sports.security.util.SecurityUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * 比赛成绩 Service 实现
 *
 * @author sports
 */
@Service
@RequiredArgsConstructor
public class CompetitionResultServiceImpl extends ServiceImpl<CompetitionResultMapper, CompetitionResult> implements CompetitionResultService {

    private final EventService eventService;
    private final SportItemService sportItemService;
    private final SysUserService sysUserService;

    @Override
    public IPage<CompetitionResult> pageResults(Integer current, Integer size, Long eventId, Long sportItemId, Long userId) {
        Page<CompetitionResult> page = new Page<>(current, size);

        LambdaQueryWrapper<CompetitionResult> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(eventId != null, CompetitionResult::getEventId, eventId)
                .eq(sportItemId != null, CompetitionResult::getSportItemId, sportItemId)
                .eq(userId != null, CompetitionResult::getUserId, userId)
                .orderByAsc(CompetitionResult::getRanking);

        return this.page(page, wrapper);
    }

    @Override
    public IPage<CompetitionResultVO> pageResultsVO(Integer current, Integer size, Long eventId, Long sportItemId, Long userId) {
        IPage<CompetitionResult> resultPage = pageResults(current, size, eventId, sportItemId, userId);
        return convertToVOPage(resultPage);
    }

    @Override
    public List<CompetitionResult> getRankingByEventAndItem(Long eventId, Long sportItemId) {
        LambdaQueryWrapper<CompetitionResult> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(CompetitionResult::getEventId, eventId)
                .eq(CompetitionResult::getSportItemId, sportItemId)
                .orderByAsc(CompetitionResult::getRanking);

        return this.list(wrapper);
    }

    @Override
    public List<CompetitionResult> getMyResults(Long userId) {
        LambdaQueryWrapper<CompetitionResult> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(CompetitionResult::getUserId, userId)
                .orderByDesc(CompetitionResult::getCreateTime);

        return this.list(wrapper);
    }

    @Override
    public List<CompetitionResultVO> getMyResultsVO(Long userId) {
        List<CompetitionResult> results = getMyResults(userId);
        return convertToVOList(results);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void batchSaveResults(List<CompetitionResult> results) {
        Long recorderId = SecurityUtils.getUserId();
        for (CompetitionResult result : results) {
            result.setRecorderId(recorderId);
            applyDefaults(result);
        }
        this.saveBatch(results);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void saveResult(CompetitionResult result) {
        result.setRecorderId(SecurityUtils.getUserId());
        applyDefaults(result);
        this.save(result);
        recalculateRanking(result.getEventId(), result.getSportItemId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateResult(CompetitionResult result) {
        CompetitionResult old = result.getId() == null ? null : this.getById(result.getId());
        applyDefaults(result);
        this.updateById(result);
        if (old != null) {
            recalculateRanking(old.getEventId(), old.getSportItemId());
        }
        recalculateRanking(result.getEventId(), result.getSportItemId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteResult(Long id) {
        CompetitionResult old = this.getById(id);
        this.removeById(id);
        if (old != null) {
            recalculateRanking(old.getEventId(), old.getSportItemId());
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void recalculateRanking(Long eventId, Long sportItemId) {
        if (eventId == null || sportItemId == null) {
            return;
        }
        SportItem item = sportItemService.getById(sportItemId);
        if (item == null) {
            return;
        }
        List<CompetitionResult> results = this.list(new LambdaQueryWrapper<CompetitionResult>()
                .eq(CompetitionResult::getEventId, eventId)
                .eq(CompetitionResult::getSportItemId, sportItemId));
        if (results.isEmpty()) {
            return;
        }

        String type = item.getScoreType();
        boolean winLoss = "WIN_LOSS".equalsIgnoreCase(type);
        boolean asc = "TIME".equalsIgnoreCase(type) || "ASC".equalsIgnoreCase(item.getSortRule());

        if (winLoss) {
            // 胜负类：先看胜负，再看得分/局数
            results.sort(Comparator
                    .comparingInt((CompetitionResult r) -> r.getIsWin() == null ? 0 : r.getIsWin())
                    .reversed()
                    .thenComparing(CompetitionResult::getScore,
                            Comparator.nullsLast(Comparator.reverseOrder())));
        } else if (asc) {
            results.sort(Comparator.comparing(CompetitionResult::getScore,
                    Comparator.nullsLast(Comparator.naturalOrder())));
        } else {
            results.sort(Comparator.comparing(CompetitionResult::getScore,
                    Comparator.nullsLast(Comparator.reverseOrder())));
        }

        int rank = 0;
        CompetitionResult prev = null;
        for (int i = 0; i < results.size(); i++) {
            CompetitionResult current = results.get(i);
            boolean tie = prev != null
                    && sameScore(prev.getScore(), current.getScore())
                    && Objects.equals(prev.getIsWin(), current.getIsWin());
            if (!tie) {
                rank = i + 1;
            }
            if (!Objects.equals(current.getRanking(), rank)) {
                current.setRanking(rank);
                this.updateById(current);
            }
            prev = current;
        }
    }

    /**
     * 录入成绩时，从项目带出成绩类型和单位
     */
    private void applyDefaults(CompetitionResult result) {
        if (result.getSportItemId() == null) {
            return;
        }
        SportItem item = sportItemService.getById(result.getSportItemId());
        if (item == null) {
            return;
        }
        if (!StringUtils.hasText(result.getResultType())) {
            result.setResultType(item.getScoreType());
        }
        if (!StringUtils.hasText(result.getScoreUnit())) {
            result.setScoreUnit(item.getScoreUnit());
        }
    }

    private boolean sameScore(BigDecimal a, BigDecimal b) {
        if (a == null || b == null) {
            return a == b;
        }
        return a.compareTo(b) == 0;
    }

    @Override
    public List<CompetitionResultVO> listResultsVO(Long eventId) {
        LambdaQueryWrapper<CompetitionResult> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(eventId != null, CompetitionResult::getEventId, eventId)
                .orderByAsc(CompetitionResult::getRanking)
                .orderByAsc(CompetitionResult::getId);
        return convertToVOList(this.list(wrapper));
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Map<String, Object> importResults(Long eventId, MultipartFile file) {
        if (eventId == null) {
            throw new BusinessException("请选择赛事");
        }
        if (eventService.getById(eventId) == null) {
            throw new BusinessException(ResultCode.EVENT_NOT_FOUND);
        }
        if (file == null || file.isEmpty()) {
            throw new BusinessException("请选择 Excel 文件");
        }

        List<ResultImportRow> rows;
        try {
            rows = EasyExcel.read(file.getInputStream())
                    .head(ResultImportRow.class)
                    .sheet()
                    .doReadSync();
        } catch (Exception e) {
            throw new BusinessException("Excel 解析失败，请使用系统提供的模板");
        }

        int success = 0;
        int fail = 0;
        List<Map<String, Object>> errors = new ArrayList<>();
        Set<Long> importedItemIds = new HashSet<>();
        Long recorderId = SecurityUtils.getUserId();

        for (int i = 0; i < rows.size(); i++) {
            ResultImportRow row = rows.get(i);
            int rowNo = i + 2;
            try {
                if (!StringUtils.hasText(row.getStudentNo())) {
                    throw new IllegalArgumentException("学号为空");
                }
                if (!StringUtils.hasText(row.getSportItemName())) {
                    throw new IllegalArgumentException("项目名称为空");
                }
                if (row.getScore() == null) {
                    throw new IllegalArgumentException("成绩为空");
                }

                List<SysUser> users = sysUserService.lambdaQuery()
                        .eq(SysUser::getStudentNo, row.getStudentNo().trim())
                        .list();
                if (users.isEmpty()) {
                    throw new IllegalArgumentException("学号不存在：" + row.getStudentNo());
                }
                SysUser user = users.get(0);

                List<SportItem> items = sportItemService.lambdaQuery()
                        .eq(SportItem::getEventId, eventId)
                        .eq(SportItem::getName, row.getSportItemName().trim())
                        .list();
                if (items.isEmpty()) {
                    throw new IllegalArgumentException("项目不存在：" + row.getSportItemName());
                }
                SportItem item = items.get(0);

                CompetitionResult result = new CompetitionResult();
                result.setEventId(eventId);
                result.setSportItemId(item.getId());
                result.setUserId(user.getId());
                result.setScore(row.getScore());
                result.setScoreUnit(StringUtils.hasText(row.getUnit()) ? row.getUnit() : item.getScoreUnit());
                result.setResultType(item.getScoreType());
                result.setRanking(row.getRanking());
                result.setPoints(row.getPoints() == null ? 0 : row.getPoints());
                result.setRemark(row.getRemark());
                result.setRecorderId(recorderId);
                this.save(result);
                importedItemIds.add(item.getId());
                success++;
            } catch (Exception e) {
                fail++;
                Map<String, Object> error = new HashMap<>();
                error.put("row", rowNo);
                error.put("message", e.getMessage());
                errors.add(error);
            }
        }

        for (Long itemId : importedItemIds) {
            recalculateRanking(eventId, itemId);
        }

        Map<String, Object> summary = new HashMap<>();
        summary.put("total", rows.size());
        summary.put("success", success);
        summary.put("fail", fail);
        summary.put("errors", errors);
        return summary;
    }

    @Override
    public Map<String, Object> getMyStatistics(Long userId) {
        List<CompetitionResult> results = getMyResults(userId);
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalEvents", results.stream()
                .map(CompetitionResult::getEventId)
                .filter(Objects::nonNull)
                .distinct()
                .count());
        stats.put("goldMedals", results.stream().filter(r -> Integer.valueOf(1).equals(r.getRanking())).count());
        stats.put("silverMedals", results.stream().filter(r -> Integer.valueOf(2).equals(r.getRanking())).count());
        stats.put("bronzeMedals", results.stream().filter(r -> Integer.valueOf(3).equals(r.getRanking())).count());
        return stats;
    }

    /**
     * 批量转换为VO（优化N+1查询）
     */
    private IPage<CompetitionResultVO> convertToVOPage(IPage<CompetitionResult> page) {
        List<CompetitionResult> records = page.getRecords();
        List<CompetitionResultVO> voList = convertToVOList(records);
        
        Page<CompetitionResultVO> voPage = new Page<>(page.getCurrent(), page.getSize(), page.getTotal());
        voPage.setRecords(voList);
        return voPage;
    }

    /**
     * 批量转换为VO列表（优化N+1查询）
     */
    private List<CompetitionResultVO> convertToVOList(List<CompetitionResult> results) {
        if (results.isEmpty()) {
            return List.of();
        }

        // 收集所有需要查询的ID
        Set<Long> eventIds = results.stream().map(CompetitionResult::getEventId).collect(Collectors.toSet());
        Set<Long> sportItemIds = results.stream().map(CompetitionResult::getSportItemId).collect(Collectors.toSet());
        Set<Long> userIds = results.stream().map(CompetitionResult::getUserId).collect(Collectors.toSet());
        Set<Long> recorderIds = results.stream()
                .map(CompetitionResult::getRecorderId)
                .filter(id -> id != null)
                .collect(Collectors.toSet());
        userIds.addAll(recorderIds);

        // 批量查询关联数据
        Map<Long, Event> eventMap = eventService.listByIds(eventIds).stream()
                .collect(Collectors.toMap(Event::getId, e -> e));
        Map<Long, SportItem> sportItemMap = sportItemService.listByIds(sportItemIds).stream()
                .collect(Collectors.toMap(SportItem::getId, s -> s));
        Map<Long, SysUser> userMap = sysUserService.listByIds(userIds).stream()
                .collect(Collectors.toMap(SysUser::getId, u -> u));

        // 转换
        return results.stream().map(result -> {
            CompetitionResultVO vo = new CompetitionResultVO();
            BeanUtils.copyProperties(result, vo);

            Event event = eventMap.get(result.getEventId());
            if (event != null) {
                vo.setEventName(event.getName());
            }

            SportItem sportItem = sportItemMap.get(result.getSportItemId());
            if (sportItem != null) {
                vo.setSportItemName(sportItem.getName());
            }

            SysUser user = userMap.get(result.getUserId());
            if (user != null) {
                vo.setUsername(user.getUsername());
                vo.setRealName(user.getRealName());
                vo.setStudentNo(user.getStudentNo());
                vo.setCollege(user.getCollege());
            }

            vo.setUnit(result.getScoreUnit());

            if (result.getRecorderId() != null) {
                SysUser recorder = userMap.get(result.getRecorderId());
                if (recorder != null) {
                    vo.setRecorderName(recorder.getRealName());
                }
            }

            return vo;
        }).collect(Collectors.toList());
    }
}