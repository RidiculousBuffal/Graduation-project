<template>
  <div>
    <!-- 搜索栏 -->
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-row>
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
          <el-form-item label="机号" prop="AircraftID">
            <el-input
                v-model="queryParams.AircraftID"
                placeholder="请输入机号"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery"
            />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="航班状态" prop="FlightStatus">
            <el-select
                v-model="queryParams.FlightStatus"
                placeholder="请输入航班状态"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery">
              <el-option v-for="item in flightStatusList" :key="item.dictValue"
                         :value="item.dictValue" :label="item.dictLabel"></el-option>
            </el-select>
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
      <el-col :span="1.5">
        <el-button
            type="success"
            plain
            icon="el-icon-upload2"
            size="mini"
            @click="handleImport"
        >导入</el-button>
      </el-col>
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
    <!-- 表格区域 -->
    <el-table v-loading="loading" :data="flightList" @selection-change="handleSelectionChange">
      <!-- 多选框 -->
      <el-table-column type="selection" width="55" align="center" />
      <!-- 序号列 -->
      <el-table-column label="序号" width="60" align="center" :formatter="indexMethod"></el-table-column>
      <!-- 基础信息 -->
      <el-table-column label="航班号" align="center" prop="FlightID"  v-if="columns[0].visible"/>
      <el-table-column label="机号" align="center" prop="AircraftID"  v-if="columns[1].visible"/>
      <el-table-column label="飞机型号" align="center" prop="AircraftModel"  v-if="columns[2].visible"/>
      <el-table-column label="机龄" align="center" prop="AircraftAge"  v-if="columns[3].visible"/>
      <el-table-column label="航站" align="center" prop="Terminal"  v-if="columns[4].visible"/>
      <el-table-column label="航班状态" align="center" prop="FlightStatus"  v-if="columns[5].visible">
        <template slot-scope="scope">
          <el-tag :style="getStatusTagType(scope.row.FlightStatus)">
            {{ scope.row.FlightStatus }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="预计起飞时间" prop="EstimatedDeparture" align="center"  v-if="columns[6].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedDeparture ? formatTime(scope.row.EstimatedDeparture) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="预计落地时间" prop="EstimatedArrival" align="center"  v-if="columns[7].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedArrival ? formatTime(scope.row.EstimatedArrival) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际起飞时间" prop="ActualDeparture" align="center"  v-if="columns[8].visible">
        <template slot-scope="scope">
          {{ scope.row.ActualDeparture ? formatTime(scope.row.ActualDeparture) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际落地时间" prop="ActualArrival" align="center"  v-if="columns[9].visible">
        <template slot-scope="scope">
          {{ scope.row.ActualArrival ? formatTime(scope.row.ActualArrival) : '-' }}
        </template>
      </el-table-column> 
      <el-table-column label="上次检测时间" prop="LastInspection" align="center"  v-if="columns[10].visible">
        <template slot-scope="scope">
          {{ formatTime(scope.row.LastInspection) }}
        </template>
      </el-table-column>
      <el-table-column label="健康状况" prop="HealthStatus" align="center"  v-if="columns[11].visible">
        <template slot-scope="scope">
          <el-tag :type="getHealthTagType(scope.row.HealthStatus)">
            {{ scope.row.HealthStatus }}
          </el-tag>
        </template>
      </el-table-column>
      <!-- 操作列 -->
      <el-table-column label="操作" align="center" width="180" fixed="right">
        <template slot-scope="scope">
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
    <!-- 添加或修改航班信息对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="700px" :close-on-click-modal="false" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="航班号" prop="FlightID">
              <el-input v-model="form.FlightID" placeholder="请输入航班号" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="机号" prop="AircraftID">
              <el-input v-model="form.AircraftID" placeholder="请输入机号" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="飞机型号" prop="AircraftModel">
              <el-input v-model="form.AircraftModel" placeholder="请输入飞机型号" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="机龄" prop="AircraftAge">
              <el-input v-model="form.AircraftAge" placeholder="请输入机龄" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="航站" prop="Terminal">
              <el-input v-model="form.Terminal" placeholder="请输入航站" maxlength="50" style="width: 200px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="航班状态" prop="FlightStatus">
              <el-select v-model="form.FlightStatus" placeholder="请选择航班状态" style="width: 200px;">
                <el-option v-for="item in flightStatusList" 
                          :key="item.dictValue"
                          :label="item.dictLabel"
                          :value="item.dictValue" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="预计起飞时间" prop="EstimatedDeparture">
              <el-date-picker
                v-model="form.EstimatedDeparture"
                type="datetime"
                placeholder="选择预计起飞时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预计落地时间" prop="EstimatedArrival">
              <el-date-picker
                v-model="form.EstimatedArrival"
                type="datetime"
                placeholder="选择预计落地时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="实际起飞时间" prop="ActualDeparture">
              <el-date-picker
                v-model="form.ActualDeparture"
                type="datetime"
                placeholder="选择实际起飞时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="实际落地时间" prop="ActualArrival">
              <el-date-picker
                v-model="form.ActualArrival"
                type="datetime"
                placeholder="选择实际落地时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="上次检测时间" prop="LastInspection">
              <el-date-picker
                v-model="form.LastInspection"
                type="datetime"
                placeholder="选择上次检测时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                style="width: 200px;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="健康状况" prop="HealthStatus">
              <el-select v-model="form.HealthStatus" placeholder="请选择健康状况" style="width: 200px;">
                <el-option label="良好" value="良好" />
                <el-option label="一般" value="一般" />
                <el-option label="较差" value="较差" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancel">取 消</el-button>
        <el-button type="primary" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "AirlineManage",
  data(){
    return {
      // 搜索栏显示
      showSearch: true,
      // 遮罩层
      loading: false,
      // 航班信息表格数据
      flightList: [
      {
          FlightID: 'CA1234',
          AircraftID: 'B-6543',
          AircraftModel: 'A320',
          AircraftAge: 5,
          Terminal: 'T2',
          EstimatedDeparture: '2023-05-10T08:00:00',
          EstimatedArrival: '2023-05-10T11:00:00',
          ActualDeparture: '2023-05-10T08:15:00',
          ActualArrival: '2023-05-10T11:20:00',
          FlightStatus: '待进港',
          LastInspection: '2023-04-28T14:00:00',
          HealthStatus: '较差'
        },
        {
          FlightID: 'MU5678',
          AircraftID: 'B-2233',
          AircraftModel: 'B737',
          AircraftAge: 3,
          Terminal: 'T1',
          EstimatedDeparture: '2023-05-10T09:30:00',
          EstimatedArrival: '2023-05-10T12:40:00',
          ActualDeparture: '2023-05-10T09:25:00',
          ActualArrival: '2023-05-10T12:35:00',
          FlightStatus: '巡检中',
          LastInspection: '2023-05-01T10:00:00',
          HealthStatus: '良好'
        }
      ],
      // 航班状态列表
      flightStatusList: [],
      // 总条数
      total: 2,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        FlightID: '',
        AircraftID: '',
        AircraftModel:'',
        AircraftAge: '',
        Terminal: '',
        EstimatedDeparture: '',
        EstimatedArrival: '',
        FlightStatus: '',
        ActualDeparture: '',
        ActualArrival: '',
        LastInspection:'',
        HealthStatus: '',
        ApprovalStatus: '',
        CreatedAt: '',
        UpdatedAt: ''
      },
      columns: [
        { key: 0, label: `航班号`, visible: true },
        { key: 1, label: `机号`, visible: true },
        { key: 2, label: `飞机型号`, visible: false },
        { key: 3, label: `机龄`, visible: true },
        { key: 4, label: `航站`, visible: false },
        { key: 5, label: `航班状态`, visible: true },
        { key: 6, label: `预计起飞时间`, visible: true },
        { key: 7, label: `预计落地时间`, visible: false },
        { key: 8, label: `实际起飞时间`, visible: false },
        { key: 9, label: `实际落地时间`, visible: false },
        { key: 10, label: `上次检测时间`, visible: true },
        { key: 11, label: `健康状况`, visible: true },
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
    
    // /航班状态标签颜色
  getStatusTagType(status) {
    const styleMap = {
      '延误': { 
        backgroundColor: '#FFEEEE', // 浅红色背景
        color: '#F56C6C',          // 深红色文字
      },
      '待进港': { 
        backgroundColor: '#F5F7FA', // 浅灰色背景
        color: '#606266',           // 深灰色文字
      },
      '已离港': { 
        backgroundColor: '#F0F9EB', // 浅绿色背景
        color: '#67C23A',           // 深绿色文字
      },
      '巡检中': { 
        backgroundColor: '#FDF6E9', // 浅黄色背景
        color: '#E6A23C',           // 深黄色文字
      }
    };
    return styleMap[status] || {};
  },
    // 健康状态标签颜色
    getHealthTagType(status) {
      const map = {
        '良好': 'success',  // 绿色
        '一般': 'warning',  // 黄色
        '较差': 'danger'    // 红色
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
        flightNumber: '',
        aircraftNumber: '',
        flightStatus: '',
       
      };
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 表单重置
    reset() {
      this.form = {
        id:'',
        FlightID: '',
        AircraftID: '',
        AircraftModel:'',
        AircraftAge: '',
        Terminal: '',
        EstimatedDeparture: '',
        EstimatedArrival: '',
        FlightStatus: '',
        ActualDeparture: '',
        ActualArrival: '',
        LastInspection:'',
        HealthStatus: '',
        ApprovalStatus: ''      
      };
      this.resetForm("form");
    },

    // 新增
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加航线信息";
    },
    // 修改
    handleUpdate(row) {
      this.reset();
      // const id = row.id;
      // getAirline(id).then(response => {
      //   console.log(response.data)
      //   this.form = response.data;
      //   this.open = true;
      //   this.title = "修改航线信息";
      // });
      this.form=row;
      this.open = true;
      this.title = "修改航线信息";


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
    // 删除
    handleDelete(row) {
      const names = row.FlightID;
      const ids = row.id;
      this.$modal.confirm('是否确认删除航班号为"' + names + '"的数据项？').then(function() {
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
  //  导入
    handleImport() {
      // this.upload.title = "航班信息导入";
      // this.importForm.projectId = this.currentProject.projectId;
      // this.upload.open = true;
    },
  }
}
</script>

<style scoped>

</style>