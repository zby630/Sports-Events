package com.sports.modules.match.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.sports.modules.match.entity.SportMatch;
import com.sports.modules.match.vo.SportMatchVO;

/**
 * 对阵 Service
 *
 * @author sports
 */
public interface SportMatchService extends IService<SportMatch> {

    /**
     * 分页查询对阵
     */
    IPage<SportMatchVO> pageMatches(Integer current, Integer size, Long eventId,
                                    Long sportItemId, Integer status);

    /**
     * 新增对阵（自动判定胜者）
     */
    void saveMatch(SportMatch match);

    /**
     * 修改对阵（自动判定胜者）
     */
    void updateMatch(SportMatch match);

    /**
     * 删除对阵
     */
    void deleteMatch(Long id);
}
