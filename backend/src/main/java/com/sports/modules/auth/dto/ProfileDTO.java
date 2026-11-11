package com.sports.modules.auth.dto;

import lombok.Data;

/**
 * 个人资料修改 DTO
 *
 * @author sports
 */
@Data
public class ProfileDTO {

    private String realName;

    private String studentNo;

    private String phone;

    private String email;

    /**
     * 学院
     */
    private String college;

    /**
     * 学院（前端旧字段别名）
     */
    private String department;

    private String className;

    /**
     * 性别：M-男 F-女
     */
    private String gender;
}
