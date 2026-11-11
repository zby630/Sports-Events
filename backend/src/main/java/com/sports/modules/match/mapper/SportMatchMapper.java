package com.sports.modules.match.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.sports.modules.match.entity.SportMatch;
import org.apache.ibatis.annotations.Mapper;

/**
 * 对阵 Mapper
 *
 * @author sports
 */
@Mapper
public interface SportMatchMapper extends BaseMapper<SportMatch> {
}
