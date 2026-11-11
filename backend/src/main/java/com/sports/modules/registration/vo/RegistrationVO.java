package com.sports.modules.registration.vo;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 报名 VO
 *
 * @author sports
 */
@Data
public class RegistrationVO {

    private Long id;
    private Long eventId;
    private String eventName;
    private Long sportItemId;
    private String sportItemName;
    private Long userId;
    private String username;
    private String realName;
    private String studentNo;
    private String college;
    private String phone;
    private String status;
    private String statusName;
    private Long reviewerId;
    private String reviewerName;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime reviewTime;
    /**
     * 审核时间（前端展示字段别名）
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime auditTime;
    private String reviewRemark;
    /**
     * 审核意见（前端展示字段别名）
     */
    private String auditRemark;
    private String remark;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;

    /**
     * 报名人姓名（前端展示字段别名）
     */
    public String getUserName() {
        return realName != null ? realName : username;
    }
}