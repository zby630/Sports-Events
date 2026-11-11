package com.sports.modules.result.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.sports.modules.result.entity.CompetitionResult;
import com.sports.modules.result.vo.CompetitionResultVO;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

/**
 * 比赛成绩 Service
 *
 * @author sports
 */
public interface CompetitionResultService extends IService<CompetitionResult> {

    /**
     * 分页查询成绩
     */
    IPage<CompetitionResult> pageResults(Integer current, Integer size, Long eventId, Long sportItemId, Long userId);

    /**
     * 分页查询成绩（返回VO）
     */
    IPage<CompetitionResultVO> pageResultsVO(Integer current, Integer size, Long eventId, Long sportItemId, Long userId);

    /**
     * 根据赛事和项目获取成绩排名
     */
    List<CompetitionResult> getRankingByEventAndItem(Long eventId, Long sportItemId);

    /**
     * 获取我的成绩列表
     */
    List<CompetitionResult> getMyResults(Long userId);

    /**
     * 获取我的成绩列表（返回VO）
     */
    List<CompetitionResultVO> getMyResultsVO(Long userId);

    /**
     * 批量录入成绩
     */
    void batchSaveResults(List<CompetitionResult> results);

    /**
     * 录入单条成绩（自动带出项目成绩类型，并重算名次）
     */
    void saveResult(CompetitionResult result);

    /**
     * 修改成绩（并重算名次）
     */
    void updateResult(CompetitionResult result);

    /**
     * 删除成绩（并重算名次）
     */
    void deleteResult(Long id);

    /**
     * 按项目成绩类型与排序规则重算名次
     */
    void recalculateRanking(Long eventId, Long sportItemId);

    /**
     * 查询某赛事全部成绩（含关联名称，用于导出）
     */
    List<CompetitionResultVO> listResultsVO(Long eventId);

    /**
     * Excel 导入成绩
     *
     * @return 导入统计：total/success/fail/errors
     */
    Map<String, Object> importResults(Long eventId, MultipartFile file);

    /**
     * 我的成绩统计：参赛次数、金/银/铜牌数
     */
    Map<String, Object> getMyStatistics(Long userId);
}