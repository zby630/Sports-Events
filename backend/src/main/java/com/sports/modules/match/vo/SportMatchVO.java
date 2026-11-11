package com.sports.modules.match.vo;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 对阵 VO
 *
 * @author sports
 */
@Data
public class SportMatchVO {

    private Long id;
    private Long eventId;
    private String eventName;
    private Long sportItemId;
    private String sportItemName;
    private String roundName;
    private Integer roundNo;
    private String groupNo;
    private Long player1Id;
    private String player1Name;
    private Long player2Id;
    private String player2Name;
    private Integer score1;
    private Integer score2;
    private Long winnerId;
    private String winnerName;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime matchTime;
    private String location;
    private Integer status;
    private String statusName;
    private String remark;
}
