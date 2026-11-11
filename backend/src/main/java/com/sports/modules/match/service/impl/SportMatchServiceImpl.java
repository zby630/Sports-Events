package com.sports.modules.match.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.sports.common.exception.BusinessException;
import com.sports.common.result.ResultCode;
import com.sports.modules.event.entity.Event;
import com.sports.modules.event.service.EventService;
import com.sports.modules.match.entity.SportMatch;
import com.sports.modules.match.mapper.SportMatchMapper;
import com.sports.modules.match.service.SportMatchService;
import com.sports.modules.match.vo.SportMatchVO;
import com.sports.modules.sportitem.entity.SportItem;
import com.sports.modules.sportitem.service.SportItemService;
import com.sports.modules.system.entity.SysUser;
import com.sports.modules.system.service.SysUserService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * 对阵 Service 实现
 *
 * @author sports
 */
@Service
@RequiredArgsConstructor
public class SportMatchServiceImpl extends ServiceImpl<SportMatchMapper, SportMatch> implements SportMatchService {

    private final EventService eventService;
    private final SportItemService sportItemService;
    private final SysUserService sysUserService;

    @Override
    public IPage<SportMatchVO> pageMatches(Integer current, Integer size, Long eventId,
                                           Long sportItemId, Integer status) {
        Page<SportMatch> page = new Page<>(current, size);
        LambdaQueryWrapper<SportMatch> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(eventId != null, SportMatch::getEventId, eventId)
                .eq(sportItemId != null, SportMatch::getSportItemId, sportItemId)
                .eq(status != null, SportMatch::getStatus, status)
                .orderByAsc(SportMatch::getMatchTime)
                .orderByAsc(SportMatch::getId);
        IPage<SportMatch> matchPage = this.page(page, wrapper);

        List<SportMatchVO> voList = convertToVOList(matchPage.getRecords());
        Page<SportMatchVO> voPage = new Page<>(matchPage.getCurrent(), matchPage.getSize(), matchPage.getTotal());
        voPage.setRecords(voList);
        return voPage;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void saveMatch(SportMatch match) {
        validate(match);
        fillWinner(match);
        this.save(match);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateMatch(SportMatch match) {
        if (match.getId() == null || this.getById(match.getId()) == null) {
            throw new BusinessException(ResultCode.NOT_FOUND);
        }
        validate(match);
        fillWinner(match);
        this.updateById(match);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void deleteMatch(Long id) {
        if (this.getById(id) == null) {
            throw new BusinessException(ResultCode.NOT_FOUND);
        }
        this.removeById(id);
    }

    private void validate(SportMatch match) {
        if (match.getEventId() == null || match.getSportItemId() == null) {
            throw new BusinessException("请选择赛事和运动项目");
        }
        if (match.getPlayer1Id() == null || match.getPlayer2Id() == null) {
            throw new BusinessException("请选择双方选手");
        }
        if (Objects.equals(match.getPlayer1Id(), match.getPlayer2Id())) {
            throw new BusinessException("双方选手不能相同");
        }
        if (match.getStatus() == null) {
            match.setStatus(1);
        }
    }

    /**
     * 双方比分都填写时自动判定胜者并结束比赛
     */
    private void fillWinner(SportMatch match) {
        Integer s1 = match.getScore1();
        Integer s2 = match.getScore2();
        if (s1 == null || s2 == null) {
            return;
        }
        if (s1 > s2) {
            match.setWinnerId(match.getPlayer1Id());
        } else if (s1 < s2) {
            match.setWinnerId(match.getPlayer2Id());
        } else {
            match.setWinnerId(null);
        }
        match.setStatus(3);
    }

    private List<SportMatchVO> convertToVOList(List<SportMatch> matches) {
        if (matches.isEmpty()) {
            return List.of();
        }
        Set<Long> eventIds = matches.stream().map(SportMatch::getEventId).collect(Collectors.toSet());
        Set<Long> itemIds = matches.stream().map(SportMatch::getSportItemId).collect(Collectors.toSet());
        Set<Long> userIds = matches.stream()
                .flatMap(m -> java.util.stream.Stream.of(m.getPlayer1Id(), m.getPlayer2Id(), m.getWinnerId()))
                .filter(Objects::nonNull)
                .collect(Collectors.toSet());

        Map<Long, Event> eventMap = eventService.listByIds(eventIds).stream()
                .collect(Collectors.toMap(Event::getId, e -> e));
        Map<Long, SportItem> itemMap = sportItemService.listByIds(itemIds).stream()
                .collect(Collectors.toMap(SportItem::getId, s -> s));
        Map<Long, SysUser> userMap = userIds.isEmpty() ? Map.of()
                : sysUserService.listByIds(userIds).stream().collect(Collectors.toMap(SysUser::getId, u -> u));

        return matches.stream().map(match -> {
            SportMatchVO vo = new SportMatchVO();
            BeanUtils.copyProperties(match, vo);

            Event event = eventMap.get(match.getEventId());
            if (event != null) {
                vo.setEventName(event.getName());
            }
            SportItem item = itemMap.get(match.getSportItemId());
            if (item != null) {
                vo.setSportItemName(item.getName());
            }
            vo.setPlayer1Name(userName(userMap.get(match.getPlayer1Id())));
            vo.setPlayer2Name(userName(userMap.get(match.getPlayer2Id())));
            vo.setWinnerName(userName(userMap.get(match.getWinnerId())));
            vo.setStatusName(statusName(match.getStatus()));
            return vo;
        }).collect(Collectors.toList());
    }

    private String userName(SysUser user) {
        if (user == null) {
            return null;
        }
        return StringUtils.hasText(user.getRealName()) ? user.getRealName() : user.getUsername();
    }

    private String statusName(Integer status) {
        if (status == null) {
            return "";
        }
        return switch (status) {
            case 1 -> "未开始";
            case 2 -> "进行中";
            case 3 -> "已结束";
            default -> String.valueOf(status);
        };
    }
}
