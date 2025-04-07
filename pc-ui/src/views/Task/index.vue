<template>
  <div>
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-row>
        <el-col :span="7">
          <el-form-item label="任务编号" prop="TaskID">
            <el-input
                v-model="queryParams.TaskID"
                placeholder="请输入任务编号"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery"
            />
          </el-form-item>
        </el-col>
        <el-col :span="7">
          <el-form-item label="任务状态" prop="TaskStatus">
            <el-select
                v-model="queryParams.TaskStatus"
                placeholder="请选择任务状态"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery">
              <el-option v-for="item in taskStatusList" :key="item.dictValue"
                         :value="item.dictValue" :label="item.dictLabel"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="7">
          <el-form-item label="航班号" prop="FlightID">
            <el-input
                v-model="queryParams.FlightID"
                placeholder="请输入航班号"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row type="flex" justify="end">
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">查询</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-row>
    </el-form>
    <el-row :gutter="10">
      <el-col :span="1.5">
        <el-button
            type="primary"
            plain
            icon="el-icon-plus"
            size="mini"
            @click="handleAdd"
        >新增</el-button>
      </el-col>
      <!-- <el-col :span="1.5">
        <el-button
            type="success"
            plain
            icon="el-icon-upload2"
            size="mini"
            @click="handleImport"
        >导入</el-button>
      </el-col> -->
      <el-col :span="1.5">
        <el-button
            type="warning"
            plain
            icon="el-icon-download"
            size="mini"
            @click="handleExport"
        >导出</el-button>
      </el-col>
    </el-row>
    <el-table v-loading="loading" :data="taskList" @selection-change="handleSelectionChange">
      <!-- 多选框 -->
      <el-table-column type="selection" width="55" align="center" />
      <!-- 序号列 -->
      <el-table-column label="序号" width="50" align="center">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
     
      <!-- 基础信息 -->
      <el-table-column label="任务编号" align="center" prop="TaskID" width="140" v-if="columns[0].visible"/>
      <el-table-column label="航班号" align="center" prop="FlightID" width="140" v-if="columns[1].visible"/>
      <el-table-column label="工程师" align="center" prop="Engineer" width="140" v-if="columns[2].visible"/>
      <el-table-column label="任务状态" align="center" prop="TaskStatus" width="140" v-if="columns[3].visible">
        <template slot-scope="scope">
          <el-tag :style="getStatusTagType(scope.row.TaskStatus)">
            {{ scope.row.TaskStatus }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="预计开始时间" prop="EstimatedStart" align="center" width="180" v-if="columns[4].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedStart ? formatTime(scope.row.EstimatedStart) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="预计结束时间" prop="EstimatedEnd" align="center" width="180" v-if="columns[5].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedEnd ? formatTime(scope.row.EstimatedEnd) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际开始时间" prop="ActualStart" align="center" width="180" v-if="columns[6].visible">
        <template slot-scope="scope">
          {{ scope.row.ActualStart ? formatTime(scope.row.ActualStart) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际结束时间" prop="ActualEnd" align="center" width="180" v-if="columns[7].visible">
        <template slot-scope="scope">
          {{ scope.row.ActualEnd ? formatTime(scope.row.ActualEnd) : '-' }}
        </template>
      </el-table-column> 
      <!-- 操作列 -->
      <el-table-column label="操作" align="center" width="180" fixed="right">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-user-solid"
            @click.stop="assignTask(scope.row)"
          >分配</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click.stop="handleUpdate(scope.row)"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "Task",
  data(){
    return{
      // 搜索栏显示
      showSearch: true,
      // 遮罩层
      loading: false,
      // 航班信息表格数据
      taskList: [
      {
        "TaskID": "T1001",
        "FlightID": "AA101",
        "EstimatedStart": "2023-11-05 09:00",
        "EstimatedEnd": "2023-11-05 09:45",
        "ActualStart": "2023-11-05 09:10",
        "ActualEnd": "2023-11-05 09:50",
        "Engineer": "Alice Brown",
        "TaskStatus": "已分配"
      },
      {  
        "TaskID": "T1002",
        "FlightID": "BA202",
        "EstimatedStart": "2023-11-05 14:30",
        "EstimatedEnd": "2023-11-05 15:30",
        "ActualStart": "",
        "ActualEnd": "",
        "Engineer": "Bob Smith",
        "TaskStatus": "待分配"
      }
      ],
      // 飞机列表
      aircraftList: [],
      // 任务状态列表
      taskStatusList: [],
      // 总条数
      total: 0,
       // 查询参数
       queryParams: {
        pageNum: 1,
        pageSize: 10,
        TaskID: '',
        FlightID: '',
        EstimatedStart: '',
        EstimatedEnd: '',
        ActualStart: '',
        ActualEnd: '',
        Engineer:'',
        TaskStatus:'',
        CreatedAt: '',
        UpdatedAt: ''
      },
      columns: [
        { key: 0, label: `任务编号`, visible: true },
        { key: 1, label: `航班号`, visible: true },
        { key: 2, label: `工程师`, visible: true },
        { key: 3, label: `任务状态`, visible: true },
        { key: 4, label: `预计开始时间`, visible: true },
        { key: 5, label: `预计结束时间`, visible: false },
        { key: 6, label: `实际开始时间`, visible: false },
        { key: 7, label: `实际结束时间`, visible: false }
      ],
    }
  },
  methods: {
    // 分页后序号连续显示
    indexMethod(row, column, cellValue, index) {
      return (this.queryParams.pageNum - 1) * this.queryParams.pageSize + index + 1;
    },
    // 时间格式化
    formatTime(time) {
      if (!time) return '-';
      return new Date(time).toLocaleString();
    },
    
    // 航班状态标签颜色
    getStatusTagType(status) {
      const map = {
      '待开始': { 
        backgroundColor: '#ECF5FF', // 浅蓝色背景
        color: '#409EFF',          // 深蓝色文字
      },
      '待分配': { 
        backgroundColor: '#F5F7FA', // 浅灰色背景
        color: '#606266',           // 深灰色文字
      },
      '已完成': { 
        backgroundColor: '#F0F9EB', // 浅绿色背景
        color: '#67C23A',           // 深绿色文字
      },
      '进行中': { 
        backgroundColor: '#FDF6E9', // 浅黄色背景
        color: '#E6A23C',           // 深黄色文字
      }
    };
      return map[status] || '';
    },
        
    // 查询
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    // 重置
    resetQuery() {
      this.queryParams = {
        flightNumber: '',
        aircraftNumber: '',
        flightStatus: '',
        pageNum: 1,
        pageSize: 10
      };
      this.handleQuery();
    },
    // 获取表格数据接口
    getList() {
      // 模拟接口请求
      this.loading = true;
      setTimeout(() => {
        this.loading = false;
      }, 500);
    },
    // 修改
    handleUpdate() {
      
    },
    // 删除
    handleDelete(row) {
      this.$confirm('确认删除该航班记录?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('删除成功');
      }).catch(() => {
        this.$message.info('已取消删除'); 
      });
    }
  }
}
</script>

<style scoped>

</style>