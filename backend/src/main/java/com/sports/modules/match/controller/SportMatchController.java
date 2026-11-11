package com.sports.modules.match.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.sports.common.result.Result;
import com.sports.modules.match.entity.SportMatch;
import com.sports.modules.match.service.SportMatchService;
import com.sports.modules.match.vo.SportMatchVO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

/**
 * 对阵管理 Controller
 *
 * @author sports
 */
@Tag(name = "对阵管理", description = "球类项目的双方对阵与比分")
@RestController
@RequestMapping("/api/matches")
@RequiredArgsConstructor
public class SportMatchController {

    private final SportMatchService sportMatchService;

    @Operation(summary = "分页查询对阵")
    @GetMapping
    public Result<IPage<SportMatchVO>> pageMatches(
            @RequestParam(defaultValue = "1") Integer current,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) Long eventId,
            @RequestParam(required = false) Long sportItemId,
            @RequestParam(required = false) Integer status) {
        return Result.success(sportMatchService.pageMatches(current, size, eventId, sportItemId, status));
    }

    @Operation(summary = "获取对阵详情")
    @GetMapping("/{id}")
    public Result<SportMatch> getById(@PathVariable Long id) {
        return Result.success(sportMatchService.getById(id));
    }

    @Operation(summary = "新增对阵")
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'TEACHER')")
    public Result<Long> create(@Valid @RequestBody SportMatch match) {
        sportMatchService.saveMatch(match);
        return Result.success(match.getId());
    }

    @Operation(summary = "修改对阵")
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'TEACHER')")
    public Result<Void> update(@PathVariable Long id, @Valid @RequestBody SportMatch match) {
        match.setId(id);
        sportMatchService.updateMatch(match);
        return Result.success();
    }

    @Operation(summary = "删除对阵")
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public Result<Void> delete(@PathVariable Long id) {
        sportMatchService.deleteMatch(id);
        return Result.success();
    }
}
