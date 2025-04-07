<template>
  <div>
    <!-- 搜索栏 -->
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-row>
        <el-col :span="6">
          <el-form-item label="机号" prop="AircraftID">
            <el-input
                v-model="queryParams.AircraftID"
                placeholder="请输入机号"
                clearable
                maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery"
            />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="检测状态" prop="InceptionStatus">
            <el-select
                v-model="queryParams.InceptionStatus"
                placeholder="请选择检测状态"
                clearable
                style="width: 200px;"
                @keyup.enter.native="handleQuery">
              <el-option label="进行中" value="进行中" />
              <el-option label="已完成" value="已完成" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="执行人" prop="Executor">
            <el-input
                v-model="queryParams.Executor"
                placeholder="请输入执行人"
                clearable
                maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery"
            />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item style="position: absolute; right: 1%">
            <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">查询</el-button>
            <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
     <!-- 功能按钮 -->
     <el-row :gutter="10" style="margin-bottom: 10px;">
      <!-- <el-col :span="1.5">
        <el-button
            type="primary"
            plain
            icon="el-icon-plus"
            size="mini"
            @click="handleAdd"
        >新增</el-button>
      </el-col> -->
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
    <el-table v-loading="loading" :data="inspectionList" @selection-change="handleSelectionChange">
      <!-- 多选框 -->
      <el-table-column type="selection" width="55" align="center" />
      
      <!-- 序号列 -->
      <el-table-column label="序号" width="50" align="center" :formatter="indexMethod"></el-table-column>
      
      <!-- 检测记录字段 -->
      <el-table-column label="检测编号" align="center" prop="InceptionID" v-if="columns[0].visible"/>
      
      <el-table-column label="机号" align="center" prop="AircraftID" v-if="columns[1].visible"/>
      
      <el-table-column label="执行人" align="center" prop="Executor" v-if="columns[2].visible"/>
      
      <el-table-column label="作业进度" align="center" prop="Progress" v-if="columns[3].visible">
        <template slot-scope="scope">
          <el-progress 
            :percentage="scope.row.Progress" 
            :status="getProgressStatus(scope.row.Progress)"
            :text-inside="true"
            :stroke-width="18"
            style="width: 80%"/>
        </template>
      </el-table-column>
      
      <el-table-column label="检测开始时间" align="center" prop="StartTime" v-if="columns[4].visible">
        <template slot-scope="scope">
          {{ scope.row.StartTime ? formatTime(scope.row.StartTime) : '-' }}
        </template>
      </el-table-column>
      
      <el-table-column label="检测结束时间" align="center" prop="EndTime" v-if="columns[5].visible">
        <template slot-scope="scope">
          {{ scope.row.EndTime ? formatTime(scope.row.EndTime) : '-' }}
        </template>
      </el-table-column>
      
      <el-table-column label="检测状态" align="center" prop="InceptionStatus" v-if="columns[6].visible">
        <template slot-scope="scope">
          <el-tag :style="getInspectionStatusTagType(scope.row.InceptionStatus)">
            {{ scope.row.InceptionStatus }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
  
</template>

<script>
export default {
  name: "DetectRecord",
  data(){
    return{
      // 搜索栏显示
      showSearch: true,
      // 遮罩层
      loading: false,
      // 检测记录表格数据
      inspectionList: [
        {
          "InceptionID": "JC-20250407-001",
          "AircraftID": "A380-001",
          "Executor": "Zhang Wei",
          "Progress": 100,
          "StartTime": "2025-04-07 09:30:00",
          "EndTime": "2025-04-07 11:45:00",
          "InceptionStatus": "已完成",
          "InceptionImages": "",
          "InceptionResults": ""
        },
        {
          "InceptionID": "JC-20250407-002",
          "AircraftID": "B787-005",
          "Executor": "Li Fang",
          "Progress": 30,
          "StartTime": "2025-04-07 14:00:00",
          "EndTime": null,
          "InceptionStatus": "进行中",
          "InceptionImages": "",
          "InceptionResults": ""
        }
      ],
      // 检测状态列表
      InceptionStatusList: [],
      // 总条数
      total: 2,
       // 查询参数
       queryParams: {
        pageNum: 1,
        pageSize: 10,
        InceptionID: '',
        AircraftID: '',
        Executor: '',
        Progress: '',
        InceptionImages: '',
        InceptionResults: '',
        StartTime:'',
        EndTime:'',
        InceptionStatus: '',
        CreatedAt: '',
        UpdatedAt: ''
      },
      columns: [
        { key: 0, label: `检测编号`, visible: true },
        { key: 1, label: `机号`, visible: true },
        { key: 2, label: `执行人`, visible: true },
        { key: 3, label: `作业进度`, visible: true },
        { key: 4, label: `检测开始时间`, visible: true },
        { key: 5, label: `检测结束时间`, visible: true },
        { key: 6, label: `检测状态`, visible: true },
        { key: 7, label: `各点位检测图`, visible: false },
        { key: 8, label: `各点位检测图结果`, visible: false }
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 表单参数
      form: {},
      // 表单校验
      rules: {},
    }
  },
  created() {
      this.getList();
    },
    methods: {
      // 获取表格数据接口
    getList() {
      // 模拟接口请求
      this.loading = true;
      setTimeout(() => {
        this.loading = false;
      }, 500);
    },
    // 分页后序号连续显示
    indexMethod(row, column, cellValue, index) {
      return (this.queryParams.pageNum - 1) * this.queryParams.pageSize + index + 1;
    },
    // 时间格式化
    formatTime(time) {
      if (!time) return '-';
      return new Date(time).toLocaleString();
    },
    
    // 检测状态标签颜色
    getInspectionStatusTagType(status) {
      const map = {
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
    getProgressStatus(progress) {
    if (progress >= 100) return 'success'  // 绿色（完成）
    if (progress >= 70) return 'warning'   // 黄色（警告）
    return 'exception'                     // 红色（异常/未达标）
  },
    
    // 查询按钮
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    // 重置按钮
    resetQuery() {
      this.queryParams = {
        pageNum: 1,
        pageSize: 10,
        TaskID: '',
        TaskStatus:'',
        FlightID: '',
      };
      this.resetForm("queryForm");
      this.handleQuery();
    },
    //  导出
    handleExport() {
      // this.download('system/building/export', {
      //   ...this.queryParams
      // }, `building_${new Date().getTime()}.xlsx`)
    },
 }
    
  
}
</script>

<style scoped>

</style>