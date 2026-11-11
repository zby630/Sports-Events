<template>
  <div class="page-container">
    <el-card shadow="never">
      <!-- 搜索表单 -->
      <el-form :inline="true" class="search-form">
        <el-form-item label="赛事">
          <el-select v-model="queryParams.eventId" placeholder="请选择" clearable filterable>
            <el-option v-for="item in eventOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="运动项目">
          <el-select v-model="queryParams.sportItemId" placeholder="请选择" clearable filterable>
            <el-option v-for="item in sportItemOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 操作按钮 -->
      <div class="mb-10">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>录入成绩
        </el-button>
        <el-button type="success" @click="handleExport">
          <el-icon><Download /></el-icon>导出成绩
        </el-button>
        <el-button type="warning" @click="handleImport">
          <el-icon><Upload /></el-icon>导入成绩
        </el-button>
      </div>

      <!-- 数据表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="eventName" label="赛事名称" min-width="150" />
        <el-table-column prop="sportItemName" label="运动项目" width="120" />
        <el-table-column prop="userName" label="参赛者" width="100" />
        <el-table-column prop="studentNo" label="学号" width="120" />
        <el-table-column prop="score" label="成绩" width="100" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="scoreText" label="比分/文本" width="120" />
        <el-table-column prop="isWin" label="胜负" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.isWin === 1" type="success">胜</el-tag>
            <el-tag v-else-if="row.isWin === 0" type="danger">负</el-tag>
            <span v-else>—</span>
          </template>
        </el-table-column>
        <el-table-column prop="ranking" label="名次" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.ranking === 1" type="warning">🥇 第1名</el-tag>
            <el-tag v-else-if="row.ranking === 2" type="info">🥈 第2名</el-tag>
            <el-tag v-else-if="row.ranking === 3" type="danger">🥉 第3名</el-tag>
            <span v-else>第{{ row.ranking }}名</span>
          </template>
        </el-table-column>
        <el-table-column prop="points" label="积分" width="80" />
        <el-table-column prop="recorderName" label="记录人" width="100" />
        <el-table-column prop="recordTime" label="记录时间" width="160" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        class="mt-20"
        v-model:current-page="queryParams.current"
        v-model:page-size="queryParams.size"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadData"
        @current-change="loadData"
      />
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" destroy-on-close>
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="赛事" prop="eventId">
          <el-select v-model="formData.eventId" placeholder="请选择" filterable @change="onEventChange">
            <el-option v-for="item in eventOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="运动项目" prop="sportItemId">
          <el-select v-model="formData.sportItemId" placeholder="请选择" filterable @change="onSportItemChange">
            <el-option v-for="item in formSportItemOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="参赛者" prop="userId">
          <el-select v-model="formData.userId" placeholder="请选择" filterable>
            <el-option v-for="item in participantOptions" :key="item.userId" :label="item.userName" :value="item.userId" />
          </el-select>
        </el-form-item>
        <el-form-item label="成绩类型">
          <el-tag type="info">{{ resultTypeName }}</el-tag>
          <span class="form-tip">由所属项目决定</span>
        </el-form-item>
        <el-form-item v-if="formData.resultType === 'WIN_LOSS'" label="胜负" prop="isWin">
          <el-radio-group v-model="formData.isWin">
            <el-radio :label="1">胜</el-radio>
            <el-radio :label="0">负</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item :label="scoreLabel" prop="score">
          <el-input-number v-model="formData.score" :precision="2" :step="0.1" />
        </el-form-item>
        <el-form-item v-if="formData.resultType === 'WIN_LOSS'" label="比分" prop="scoreText">
          <el-input v-model="formData.scoreText" placeholder="如 3:1、11:9,11:7" style="width: 220px" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="formData.unit" placeholder="如：秒、米、分" style="width: 150px" />
        </el-form-item>
        <el-form-item label="名次" prop="ranking">
          <el-input-number v-model="formData.ranking" :min="1" :max="100" disabled />
          <span class="form-tip">保存后按项目规则自动计算</span>
        </el-form-item>
        <el-form-item label="积分" prop="points">
          <el-input-number v-model="formData.points" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="formData.remark" type="textarea" :rows="2" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 导入弹窗 -->
    <el-dialog v-model="importDialogVisible" title="导入成绩" width="500px">
      <el-form label-width="100px">
        <el-form-item label="赛事">
          <el-select v-model="importEventId" placeholder="请选择" filterable>
            <el-option v-for="item in eventOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="选择文件">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            accept=".xlsx,.xls"
            :on-change="handleFileChange"
          >
            <el-button type="primary">选择Excel文件</el-button>
            <template #tip>
              <div class="el-upload__tip">只能上传 xlsx/xls 文件</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" link @click="downloadTemplate">下载导入模板</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="importLoading" @click="submitImport">确定导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules, UploadInstance } from 'element-plus'
import { get, post, put, del } from '@/utils/request'
import service from '@/utils/request'

const loading = ref(false)
const tableData = ref<any[]>([])
const total = ref(0)
const eventOptions = ref<any[]>([])
const sportItemOptions = ref<any[]>([])

const queryParams = reactive({
  current: 1,
  size: 10,
  eventId: null as number | null,
  sportItemId: null as number | null
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const submitLoading = ref(false)
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)

const formSportItemOptions = ref<any[]>([])
const participantOptions = ref<any[]>([])

const formData = reactive({
  eventId: null as number | null,
  sportItemId: null as number | null,
  userId: null as number | null,
  score: 0,
  unit: '',
  resultType: 'SCORE',
  scoreText: '',
  isWin: null as number | null,
  ranking: 1,
  points: 0,
  remark: ''
})

const resultTypeName = computed(() => {
  const map: Record<string, string> = {
    TIME: '计时（越小越好）',
    DISTANCE: '计距（越大越好）',
    SCORE: '计分（越大越好）',
    WIN_LOSS: '胜负（球类）'
  }
  return map[formData.resultType] || formData.resultType || '未设置'
})

const scoreLabel = computed(() => {
  const map: Record<string, string> = {
    TIME: '成绩（秒）',
    DISTANCE: '成绩（米）',
    SCORE: '得分',
    WIN_LOSS: '胜局/得分'
  }
  return map[formData.resultType] || '成绩'
})

const rules: FormRules = {
  eventId: [{ required: true, message: '请选择赛事', trigger: 'change' }],
  sportItemId: [{ required: true, message: '请选择运动项目', trigger: 'change' }],
  userId: [{ required: true, message: '请选择参赛者', trigger: 'change' }],
  score: [{ required: true, message: '请输入成绩', trigger: 'blur' }]
}

const importDialogVisible = ref(false)
const importLoading = ref(false)
const importEventId = ref<number | null>(null)
const uploadRef = ref<UploadInstance>()
const importFile = ref<File | null>(null)

onMounted(() => {
  loadEventOptions()
  loadData()
})

async function loadEventOptions() {
  const res = await get('/events', { size: 100 })
  if (res.code === 200) {
    eventOptions.value = res.data.records || []
  }
}

async function loadData() {
  loading.value = true
  try {
    const res = await get('/results', queryParams)
    if (res.code === 200) {
      tableData.value = res.data.records
      total.value = res.data.total
    }
  } finally {
    loading.value = false
  }
}

function resetQuery() {
  queryParams.eventId = null
  queryParams.sportItemId = null
  queryParams.current = 1
  loadData()
}

function handleAdd() {
  editingId.value = null
  dialogTitle.value = '录入成绩'
  Object.assign(formData, {
    eventId: null, sportItemId: null, userId: null,
    score: 0, unit: '', resultType: 'SCORE', scoreText: '', isWin: null,
    ranking: 1, points: 0, remark: ''
  })
  formSportItemOptions.value = []
  participantOptions.value = []
  dialogVisible.value = true
}

async function handleEdit(row: any) {
  editingId.value = row.id
  dialogTitle.value = '编辑成绩'
  await onEventChange(row.eventId)
  await onSportItemChange(row.sportItemId)
  Object.assign(formData, row)
  if (!formData.resultType) {
    const item = formSportItemOptions.value.find((x: any) => x.id === row.sportItemId)
    formData.resultType = item?.scoreType || 'SCORE'
  }
  dialogVisible.value = true
}

async function onEventChange(eventId: number) {
  formData.sportItemId = null
  formData.userId = null
  participantOptions.value = []
  if (eventId) {
    const res = await get('/sport-items', { eventId, size: 100 })
    if (res.code === 200) {
      formSportItemOptions.value = res.data.records || []
    }
  } else {
    formSportItemOptions.value = []
  }
}

async function onSportItemChange(sportItemId: number) {
  formData.userId = null
  const item = formSportItemOptions.value.find((x: any) => x.id === sportItemId)
  if (item) {
    formData.resultType = item.scoreType || 'SCORE'
    formData.unit = item.scoreUnit || ''
    formData.isWin = null
    formData.scoreText = ''
  }
  if (sportItemId) {
    // 获取该项目已通过审核的报名人员
    const res = await get('/registrations', { sportItemId, status: 'APPROVED', size: 100 })
    if (res.code === 200) {
      participantOptions.value = res.data.records || []
    }
  } else {
    participantOptions.value = []
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    submitLoading.value = true
    try {
      if (editingId.value) {
        await put(`/results/${editingId.value}`, formData)
        ElMessage.success('更新成功')
      } else {
        await post('/results', formData)
        ElMessage.success('录入成功')
      }
      dialogVisible.value = false
      loadData()
    } finally {
      submitLoading.value = false
    }
  })
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm('确定要删除该成绩记录吗？', '提示', { type: 'warning' })
  await del(`/results/${row.id}`)
  ElMessage.success('删除成功')
  loadData()
}

async function downloadFile(url: string, params: any, fileName: string) {
  const resp: any = await service.get(url, { params, responseType: 'blob' })
  const blob = new Blob([resp.data], {
    type: resp.headers['content-type'] || 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = fileName
  link.click()
  URL.revokeObjectURL(link.href)
}

async function handleExport() {
  if (!queryParams.eventId) {
    ElMessage.warning('请先选择赛事')
    return
  }
  await downloadFile('/results/export', { eventId: queryParams.eventId }, '成绩导出.xlsx')
}

function handleImport() {
  importEventId.value = null
  importFile.value = null
  importDialogVisible.value = true
}

function handleFileChange(file: any) {
  importFile.value = file.raw
}

async function downloadTemplate() {
  await downloadFile('/results/template', undefined, '成绩导入模板.xlsx')
}

async function submitImport() {
  if (!importEventId.value) {
    ElMessage.warning('请选择赛事')
    return
  }
  if (!importFile.value) {
    ElMessage.warning('请选择文件')
    return
  }
  
  importLoading.value = true
  try {
    const formData = new FormData()
    formData.append('file', importFile.value)
    formData.append('eventId', String(importEventId.value))
    
    const res = await post('/results/import', formData)
    const summary: any = res.data || {}
    ElMessage.success(`导入完成：成功 ${summary.success ?? 0} 条，失败 ${summary.fail ?? 0} 条`)
    if (summary.errors && summary.errors.length > 0) {
      console.warn('导入失败明细', summary.errors)
    }
    importDialogVisible.value = false
    loadData()
  } finally {
    importLoading.value = false
  }
}
</script>

<style scoped>
.form-tip {
  margin-left: 10px;
  color: #94a3b8;
  font-size: 12px;
}
</style>
