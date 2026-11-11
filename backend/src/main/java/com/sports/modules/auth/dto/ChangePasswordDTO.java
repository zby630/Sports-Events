package com.sports.modules.auth.dto;

import lombok.Data;

/**
 * 修改密码 DTO
 *
 * @author sports
 */
@Data
public class ChangePasswordDTO {

    private String oldPassword;

    private String newPassword;

    private String confirmPassword;
}
