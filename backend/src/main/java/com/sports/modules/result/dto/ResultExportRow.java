package com.sports.modules.result.dto;

import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.write.style.ColumnWidth;
import lombok.Data;

import java.math.BigDecimal;

/**
 * 成绩导出行
 *
 * @author sports
 */
@Data
@ColumnWidth(18)
public class ResultExportRow {

    @ExcelProperty("赛事名称")
    private String eventName;

    @ExcelProperty("项目名称")
    private String sportItemName;

    @ExcelProperty("姓名")
    private String userName;

    @ExcelProperty("学号")
    private String studentNo;

    @ExcelProperty("成绩")
    private BigDecimal score;

    @ExcelProperty("单位")
    private String unit;

    @ExcelProperty("名次")
    private Integer ranking;

    @ExcelProperty("积分")
    private Integer points;

    @ExcelProperty("备注")
    private String remark;
}
