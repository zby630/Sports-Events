<template>
  <div class="page-container">
    <el-card shadow="never">
      <!-- 搜索 -->
      <el-form :inline="true" class="search-form">
        <el-form-item label="赛事">
          <el-select v-model="queryParams.eventId" placeholder="请选择" clearable filterable @change="onQueryEventChange">
            <el-option v-for="item in eventOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="运动项目">
          <el-select v-model="queryParams.sportItemId" placeholder="请选择" clearable filterable>
            <el-option v-for="item in queryItemOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="全部" clearable>
            <el-option label="未开始" :value="1" />
            <el-option label="进行中" :value="2" />
            <el-option label="已结束" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <div class="mb-10">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>新增对阵
        </el-button>
      </div>

      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="eventName" label="赛事" min-width="150" />
        <el-table-column prop="sportItemName" label="项目" width="120" />
        <el-table-column prop="roundName" label="轮次" width="100" />
        <el-table-column prop="groupNo" label="分组" width="80" />
        <el-table-column prop="player1Name" label="选手1" width="100" />
        <el-table-column label="比分" width="90" align="center">
          <template #default="{ row }">
            <strong>{{ row.score1 ?? '-' }} : {{ row.score2 ?? '-' }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="player2Name" label="选手2" width="100" />
        <el-table-column label="胜者" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.winnerName" type="success">{{ row.winnerName }}</el-tag>
            <span v-else>—</span>
          </template>
        </el-table-column>
        <el-table-column prop="matchTime" label="比赛时间" width="160" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ row.statusName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

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

    <!-- 新增/编辑 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px" destroy-on-close>
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="赛事" prop="eventId">
          <el-select v-model="formData.eventId" placeholder="请选择" filterable @change="onFormEventChange">
            <el-option v-for="item in eventOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="运动项目" prop="sportItemId">
          <el-select v-model="formData.sportItemId" placeholder="请选择" filterable @change="onFormItemChange">
            <el-option v-for="item in formItemOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="轮次" prop="roundName">
          <el-input v-model="formData.roundName" placeholder="如：小组赛 / 半决赛 / 决赛" style="width: 220px" />
        </el-form-item>
        <el-form-item label="轮次序号" prop="roundNo">
          <el-input-number v-model="formData.roundNo" :min="1" :max="20" />
        </el-form-item>
        <el-form-item label="分组" prop="groupNo">
          <el-input v-model="formData.groupNo" placeholder="如：A组" style="width: 160px" />
        </el-form-item>
        <el-form-item label="选手1" prop="player1Id">
          <el-select v-model="formData.player1Id" placeholder="请选择" filterable>
            <el-option v-for="p in playerOptions" :key="p.userId" :label="p.userName" :value="p.userId" />
          </el-select>
        </el-form-item>
        <el-form-item label="选手2" prop="player2Id">
          <el-select v-model="formData.player2Id" placeholder="请选择" filterable>
            <el-option v-for="p in playerOptions" :key="p.userId" :label="p.userName" :value="p.userId" />
          </el-select>
        </el-form-item>
        <el-form-item label="比分">
          <el-input-number v-model="formData.score1" :min="0" :max="999" />
          <span class="score-sep">:</span>
          <el-input-number v-model="formData.score2" :min="0" :max="999" />
          <span class="form-tip">双方比分都填后自动判定胜者</span>
        </el-form-item>
        <el-form-item label="比赛时间" prop="matchTime">
          <el-date-picker
            v-model="formData.matchTime"
            type="datetime"
            placeholder="选择时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="比赛地点" prop="location">
          <el-input v-model="formData.location" placeholder="如：体育馆1号场" />
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { get, post, put, del } from '@/utils/request'

const loading = ref(false)
const tableData = ref<any[]>([])
const total = ref(0)
const eventOptions = ref<any[]>([])
const queryItemOptions = ref<any[]>([])

const queryParams = reactive({
  current: 1,
  size: 10,
  eventId: null as number | null,
  sportItemId: null as number | null,
  status: null as number | null
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const submitLoading = ref(false)
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)

const formItemOptions = ref<any[]>([])
const playerOptions = ref<any[]>([])

const formData = reactive({
  eventId: null as number | null,
  sportItemId: null as number | null,
  roundName: '小组赛',
  roundNo: 1,
  groupNo: '',
  player1Id: null as number | null,
  player2Id: null as number | null,
  score1: null as number | null,
  score2: null as number | null,
  matchTime: '',
  location: '',
  remark: ''
})

const rules: FormRules = {
  eventId: [{ required: true, message: '请选择赛事', trigger: 'change' }],
  sportItemId: [{ required: true, message: '请选择运动项目', trigger: 'change' }],
  player1Id: [{ required: true, message: '请选择选手1', trigger: 'change' }],
  player2Id: [{ required: true, message: '请选择选手2', trigger: 'change' }]
}

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

async function loadItems(eventId: number | null, target: any) {
  if (!eventId) {
    target.value = []
    return
  }
  const res = await get('/sport-items', { eventId, size: 100 })
  if (res.code === 200) {
    target.value = res.data.records || []
  }
}

async function loadPlayers(eventId: number | null, sportItemId: number | null) {
  if (!eventId || !sportItemId) {
    playerOptions.value = []
    return
  }
  const res = await get('/registrations', { eventId, sportItemId, status: 'APPROVED', size: 200 })
  if (res.code === 200) {
    playerOptions.value = res.data.records || []
  }
}

async function onQueryEventChange(eventId: number) {
  queryParams.sportItemId = null
  await loadItems(eventId, queryItemOptions)
  loadData()
}

async function loadData() {
  loading.value = true
  try {
    const res = await get('/matches', queryParams)
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
  queryParams.status = null
  queryParams.current = 1
  queryItemOptions.value = []
  loadData()
}

function handleAdd() {
  editingId.value = null
  dialogTitle.value = '新增对阵'
  Object.assign(formData, {
    eventId: null, sportItemId: null, roundName: '小组赛', roundNo: 1,
    groupNo: '', player1Id: null, player2Id: null,
    score1: null, score2: null, matchTime: '', location: '', remark: ''
  })
  formItemOptions.value = []
  playerOptions.value = []
  dialogVisible.value = true
}

async function handleEdit(row: any) {
  editingId.value = row.id
  dialogTitle.value = '编辑对阵'
  await loadItems(row.eventId, formItemOptions)
  await loadPlayers(row.eventId, row.sportItemId)
  Object.assign(formData, row)
  dialogVisible.value = true
}

async function onFormEventChange(eventId: number) {
  formData.sportItemId = null
  formData.player1Id = null
  formData.player2Id = null
  playerOptions.value = []
  await loadItems(eventId, formItemOptions)
}

async function onFormItemChange(sportItemId: number) {
  formData.player1Id = null
  formData.player2Id = null
  await loadPlayers(formData.eventId, sportItemId)
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    if (formData.player1Id && formData.player1Id === formData.player2Id) {
      ElMessage.warning('双方选手不能相同')
      return
    }
    submitLoading.value = true
    try {
      if (editingId.value) {
        await put(`/matches/${editingId.value}`, formData)
        ElMessage.success('更新成功')
      } else {
        await post('/matches', formData)
        ElMessage.success('新增成功')
      }
      dialogVisible.value = false
      loadData()
    } finally {
      submitLoading.value = false
    }
  })
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm('确定删除该对阵吗？', '提示', { type: 'warning' })
  await del(`/matches/${row.id}`)
  ElMessage.success('删除成功')
  loadData()
}

function statusType(status: number): any {
  return status === 1 ? 'info' : status === 2 ? 'primary' : 'success'
}
</script>

<style scoped>
.score-sep {
  margin: 0 8px;
  font-size: 16px;
  color: #64748b;
}
.form-tip {
  margin-left: 10px;
  color: #94a3b8;
  font-size: 12px;
}
</style>
