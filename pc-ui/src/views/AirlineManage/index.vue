<template>
  <div>
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-row>
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
        <el-col :span="7">
          <el-form-item label="机号" prop="AircraftID">
            <el-select
                v-model="queryParams.AircraftID"
                placeholder="请输入机号"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery">
              <el-option v-for="item in aircraftList" :key="item.id"
                         :value="item.id" :label="item.name"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="7">
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
    <el-table v-loading="loading" :data="flightList" @selection-change="handleSelectionChange">
      <!-- 多选框 -->
      <el-table-column type="selection" width="55" align="center" />
      <!-- 序号列 -->
      <el-table-column label="序号" width="50" align="center">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
     
      <!-- 基础信息 -->
      <el-table-column label="航班号" align="center" prop="FlightID" width="120" v-if="columns[0].visible"/>
      <el-table-column label="机号" align="center" prop="AircraftID" width="120" v-if="columns[1].visible"/>
      <el-table-column label="飞机型号" align="center" prop="AircraftModel" width="120" v-if="columns[2].visible"/>
      <el-table-column label="机龄" align="center" prop="AircraftAge" width="120" v-if="columns[3].visible"/>
      <el-table-column label="航站" align="center" prop="Terminal" width="120" v-if="columns[4].visible"/>
      <el-table-column label="航班状态" align="center" prop="FlightStatus" width="120" v-if="columns[5].visible">
        <template slot-scope="scope">
          <el-tag :style="getStatusTagType(scope.row.FlightStatus)">
            {{ scope.row.FlightStatus }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="预计起飞时间" prop="EstimatedDeparture" align="center" width="160" v-if="columns[6].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedDeparture ? formatTime(scope.row.EstimatedDeparture) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="预计落地时间" prop="EstimatedArrival" align="center" width="160" v-if="columns[7].visible">
        <template slot-scope="scope">
          {{ scope.row.EstimatedArrival ? formatTime(scope.row.EstimatedArrival) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际起飞时间" prop="ActualDeparture" align="center" width="160" v-if="columns[8].visible">
        <template slot-scope="scope">
          {{ scope.row.ActualDeparture ? formatTime(scope.row.ActualDeparture) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="实际落地时间" prop="ActualArrival" align="center" width="160" v-if="columns[9].visible">
        <template slot-scope="scope">
          {{ scope.row.ActualArrival ? formatTime(scope.row.ActualArrival) : '-' }}
        </template>
      </el-table-column> 
      <el-table-column label="上次检测时间" prop="LastInspection" align="center" width="160" v-if="columns[10].visible">
        <template slot-scope="scope">
          {{ formatTime(scope.row.LastInspection) }}
        </template>
      </el-table-column>
      <el-table-column label="健康状况" prop="HealthStatus" align="center" width="120" v-if="columns[11].visible">
        <template slot-scope="scope">
          <el-tag :type="getHealthTagType(scope.row.HealthStatus)">
            {{ scope.row.HealthStatus }}
          </el-tag>
        </template>
      </el-table-column>
      
      <!-- 操作列 -->
      <el-table-column label="操作" align="center" width="120" fixed="right">
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
      // 飞机列表
      aircraftList: [],
      // 航班状态列表
      flightStatusList: [],
      // 总条数
      total: 0,
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