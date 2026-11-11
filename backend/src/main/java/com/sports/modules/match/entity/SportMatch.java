package com.sports.modules.match.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.sports.common.entity.BaseEntity;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.time.LocalDateTime;

/**
 * 对阵/比赛记录实体
 * 用于球类等需要记录双方比分与胜负的项目
 *
 * @author sports
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sport_match")
public class SportMatch extends BaseEntity {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    private Long id;

    /**
     * 赛事ID
     */
    private Long eventId;

    /**
     * 运动项目ID
     */
    private Long sportItemId;

    /**
     * 轮次名称（小组赛/半决赛/决赛）
     */
    private String roundName;

    /**
     * 轮次序号
     */
    private Integer roundNo;

    /**
     * 分组（A组/B组）
     */
    private String groupNo;

    /**
     * 选手/队伍1
     */
    private Long player1Id;

    /**
     * 选手/队伍2
     */
    private Long player2Id;

    /**
     * 选手1得分（局数/比分）
     */
    private Integer score1;

    /**
     * 选手2得分（局数/比分）
     */
    private Integer score2;

    /**
     * 胜者ID
     */
    private Long winnerId;

    /**
     * 比赛时间
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime matchTime;

    /**
     * 比赛地点
     */
    private String location;

    /**
     * 状态：1-未开始 2-进行中 3-已结束
     */
    private Integer status;

    /**
     * 备注
     */
    private String remark;
}
