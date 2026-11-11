package com.sports.modules.result.controller;

import com.alibaba.excel.EasyExcel;
import com.sports.common.result.PageResult;
import com.sports.common.result.Result;
import com.sports.modules.result.dto.ResultExportRow;
import com.sports.modules.result.dto.ResultImportRow;
import com.sports.modules.result.entity.CompetitionResult;
import com.sports.modules.result.service.CompetitionResultService;
import com.sports.modules.result.vo.CompetitionResultVO;
import com.sports.security.util.SecurityUtils;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * 比赛成绩 Controller
 *
 * @author sports
 */
@Tag(name = "成绩管理", description = "成绩的增删改查")
@RestController
@RequestMapping("/api/results")
@RequiredArgsConstructor
public class CompetitionResultController {

    private final CompetitionResultService competitionResultService;

    @Operation(summary = "分页查询成绩")
    @GetMapping
    public Result<PageResult<CompetitionResultVO>> pageResults(
            @RequestParam(defaultValue = "1") Integer current,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) Long eventId,
            @RequestParam(required = false) Long sportItemId,
            @RequestParam(required = false) Long userId) {
        return Result.success(PageResult.of(competitionResultService.pageResultsVO(current, size, eventId, sportItemId, userId)));
    }

    @Operation(summary = "获取成绩排名")
    @GetMapping("/ranking")
    public Result<List<CompetitionResult>> getRanking(@RequestParam Long eventId, @RequestParam Long sportItemId) {
        return Result.success(competitionResultService.getRankingByEventAndItem(eventId, sportItemId));
    }

    @Operation(summary = "获取我的成绩")
    @GetMapping("/my")
    public Result<List<CompetitionResultVO>> getMyResults() {
        Long userId = SecurityUtils.getUserId();
        return Result.success(competitionResultService.getMyResultsVO(userId));
    }

    @Operation(summary = "录入成绩")
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'TEACHER')")
    public Result<Void> saveResult(@Valid @RequestBody CompetitionResult result) {
        competitionResultService.saveResult(result);
        return Result.success();
    }

    @Operation(summary = "批量录入成绩")
    @PostMapping("/batch")
    @PreAuthorize("hasAnyRole('ADMIN', 'TEACHER')")
    public Result<Void> batchSaveResults(@RequestBody List<CompetitionResult> results) {
        competitionResultService.batchSaveResults(results);
        return Result.success();
    }

    @Operation(summary = "更新成绩")
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'TEACHER')")
    public Result<Void> updateResult(@PathVariable Long id, @Valid @RequestBody CompetitionResult result) {
        result.setId(id);
        competitionResultService.updateResult(result);
        return Result.success();
    }

    @Operation(summary = "删除成绩")
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public Result<Void> deleteResult(@PathVariable Long id) {
        competitionResultService.deleteResult(id);
        return Result.success();
    }

    @Operation(summary = "获取我的成绩统计")
    @GetMapping("/my/statistics")
    public Result<Map<String, Object>> getMyStatistics() {
        return Result.success(competitionResultService.getMyStatistics(SecurityUtils.getUserId()));
    }

    @Operation(summary = "导出成绩Excel")
    @GetMapping("/export")
    public void exportResults(@RequestParam(required = false) Long eventId,
                              HttpServletResponse response) throws IOException {
        List<ResultExportRow> rows = competitionResultService.listResultsVO(eventId).stream()
                .map(vo -> {
                    ResultExportRow row = new ResultExportRow();
                    row.setEventName(vo.getEventName());
                    row.setSportItemName(vo.getSportItemName());
                    row.setUserName(vo.getUserName());
                    row.setStudentNo(vo.getStudentNo());
                    row.setScore(vo.getScore());
                    row.setUnit(vo.getUnit());
                    row.setRanking(vo.getRanking());
                    row.setPoints(vo.getPoints());
                    row.setRemark(vo.getRemark());
                    return row;
                })
                .collect(Collectors.toList());

        String fileName = URLEncoder.encode("成绩导出.xlsx", StandardCharsets.UTF_8).replaceAll("\\+", "%20");
        response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        response.setCharacterEncoding("utf-8");
        response.setHeader("Content-Disposition", "attachment;filename*=utf-8''" + fileName);
        EasyExcel.write(response.getOutputStream(), ResultExportRow.class)
                .sheet("成绩")
                .doWrite(rows);
    }

    @Operation(summary = "下载成绩导入模板")
    @GetMapping("/template")
    public void downloadTemplate(HttpServletResponse response) throws IOException {
        String fileName = URLEncoder.encode("成绩导入模板.xlsx", StandardCharsets.UTF_8).replaceAll("\\+", "%20");
        response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        response.setCharacterEncoding("utf-8");
        response.setHeader("Content-Disposition", "attachment;filename*=utf-8''" + fileName);
        EasyExcel.write(response.getOutputStream(), ResultImportRow.class)
                .sheet("成绩导入")
                .doWrite(List.of());
    }

    @Operation(summary = "导入成绩Excel")
    @PostMapping("/import")
    @PreAuthorize("hasAnyRole('ADMIN', 'TEACHER')")
    public Result<Map<String, Object>> importResults(@RequestParam("file") MultipartFile file,
                                                     @RequestParam("eventId") Long eventId) {
        return Result.success("导入完成", competitionResultService.importResults(eventId, file));
    }
}