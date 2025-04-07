<template>
  <div>
      <!-- 搜索栏 -->
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-row>
        <el-col :span="6">
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
        <el-col :span="6">
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
        <el-col :span="6">
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
        <el-col :span="6">
          <el-form-item style="position: absolute; right: 0">
            <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">查询</el-button>
            <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
      
    </el-form>
    <!-- 功能按钮 -->
    <el-row :gutter="10" style="margin-bottom: 10px;">
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
      <el-table-column label="序号" width="50" align="center" :formatter="indexMethod"></el-table-column>
      <!-- 基础信息 -->
      <el-table-column label="任务编号" align="center" prop="TaskID" v-if="columns[0].visible"/>
      <el-table-column label="航班号" align="center" prop="FlightID"  v-if="columns[1].visible"/>
      <el-table-column label="工程师" align="center" prop="Engineer"  v-if="columns[2].visible"/>
      <el-table-column label="任务状态" align="center" prop="TaskStatus"  v-if="columns[3].visible">
        <template slot-scope="scope">
          <el-tag :style="getStatusTagType(scope.row.TaskStatus)">
            {{ scope.row.TaskStatus }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="预计开始时间" prop="EstimatedStart" align="center" v-if="columns[4].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedStart ? formatTime(scope.row.EstimatedStart) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="预计结束时间" prop="EstimatedEnd" align="center"  v-if="columns[5].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedEnd ? formatTime(scope.row.EstimatedEnd) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际开始时间" prop="ActualStart" align="center"  v-if="columns[6].visible">
        <template slot-scope="scope">
          {{ scope.row.ActualStart ? formatTime(scope.row.ActualStart) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际结束时间" prop="ActualEnd" align="center"  v-if="columns[7].visible">
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
    <pagination
        v-show="total>0"
        :total="total"
        :page.sync="queryParams.pageNum"
        :limit.sync="queryParams.pageSize"
        @pagination="getList"
    />
    <!-- 添加或修改任务信息对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="700px" :close-on-click-modal="false" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="任务编号" prop="TaskID">
              <el-input v-model="form.TaskID" placeholder="请输入任务编号" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="航班号" prop="FlightID">
              <el-input v-model="form.FlightID" placeholder="请输入航班号" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="工程师" prop="Engineer">
              <el-input v-model="form.Engineer" placeholder="请输入工程师姓名" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="任务状态" prop="TaskStatus">
              <el-select v-model="form.TaskStatus" placeholder="请选择任务状态" style="width: 200px;">
                <el-option label="待分配" value="待分配" />
                <el-option label="待开始" value="待开始" />
                <el-option label="进行中" value="进行中" />
                <el-option label="已完成" value="已完成" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="预计开始时间" prop="EstimatedStart">
              <el-date-picker
                v-model="form.EstimatedStart"
                type="datetime"
                placeholder="选择预计开始时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预计结束时间" prop="EstimatedEnd">
              <el-date-picker
                v-model="form.EstimatedEnd"
                type="datetime"
                placeholder="选择预计结束时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="实际开始时间" prop="ActualStart">
              <el-date-picker
                v-model="form.ActualStart"
                type="datetime"
                placeholder="选择实际开始时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="实际结束时间" prop="ActualEnd">
              <el-date-picker
                v-model="form.ActualEnd"
                type="datetime"
                placeholder="选择实际结束时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancel">取 消</el-button>
        <el-button type="primary" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog 
      title="分配工程师" 
      :visible.sync="assignDialogVisible" 
      width="500px"
      :close-on-click-modal="false"
      append-to-body>
      
      <!-- 单选下拉框 -->
      <el-form label-width="100px">
        <el-form-item label="工程师" prop="engineer">
          <el-select
            v-model="form.engineer"
            clearable
            placeholder="请选择工程师"
            style="width: 100%">
            <el-option
              v-for="engineer in engineerList"
              :key="engineer.id"
              :label="engineer.name"
              :value="engineer.name">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="assignCancel">取消</el-button>
        <el-button 
          type="primary" 
          @click="confirmAssign"> 
          确认分配
        </el-button>
      </div>
    </el-dialog>
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
      // 任务状态列表
      taskStatusList: [],
      // 总条数
      total: 2,
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
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 表单参数
      form: {},
      // 表单校验
      rules: {},
      assignDialogVisible:false,
      engineerList:[]
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
     // 表单重置
     reset() {
      this.form = {
        id:'',
        TaskID: '',
        FlightID: '',
        EstimatedStart: '',
        EstimatedEnd: '',
        ActualStart: '',
        ActualEnd: '',
        Engineer:'',
        TaskStatus:''
      }
      this.resetForm("form");
    },
    // 新增
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加任务信息";
    },
    // 修改
    handleUpdate(row) {
      this.reset();
      // const id = row.id;
      // getAirline(id).then(response => {
      //   console.log(response.data)
      //   this.form = response.data;
      //   this.open = true;
      //   this.title = "修改任务信息";
      // });
      this.form=row;
      this.open = true;
      this.title = "修改任务信息";


    },
    // 提交
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != '') {
            // updateAirline(this.form).then(response => {
            //   this.$modal.msgSuccess("修改成功");
            //   this.open = false;
            //   this.getList();
            // });
            this.$modal.msgSuccess("修改成功");
            this.open = false;
          } else {
            // addAirline(this.form).then(response => {
            //   this.$modal.msgSuccess("新增成功");
            //   this.open = false;
            //   this.getList();
            // });
            this.$modal.msgSuccess("新增成功");
            this.open = false;
          }
        }
      });
    },
    // 取消按钮
    cancel() {
      this.reset();
      this.open = false;
    },
    // 删除
    handleDelete(row) {
      const names = row.TaskID;
      const ids = row.id;
      this.$modal.confirm('是否确认删除任务编号为"' + names + '"的数据项？').then(function() {
        // return delAirline(ids);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    //  导出
    handleExport() {
      // this.download('system/building/export', {
      //   ...this.queryParams
      // }, `building_${new Date().getTime()}.xlsx`)
    },
    // 任务分配
    assignTask(row){
      this.assignDialogVisible=true;
    },
    // 取消
    assignCancel(){
      this.assignDialogVisible=false;
    },
    // 确认分配
    confirmAssign(){
      this.$modal.msgSuccess("分配成功");
      this.assignDialogVisible=false;
    }
  }
}
</script>

<style scoped>

</style>