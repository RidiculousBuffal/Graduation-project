<template>
  <div>
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-row>
        <el-col :span="8">
          <el-form-item label="航班号" prop="flightId">
            <el-input
                v-model="queryParams.flightId"
                placeholder="请输入航班号"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="机号" prop="aircraftId">
            <el-select
                v-model="queryParams.aircraftId"
                placeholder="请输入机号"
                clearable maxlength="50"
                style="width: 200px;"
                @keyup.enter.native="handleQuery">
              <el-option v-for="item in aircraftList" :key="item.id"
                         :value="item.id" :label="item.name"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="航班状态" prop="flightStatus">
            <el-select
                v-model="queryParams.flightStatus"
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
            type="info"
            plain
            icon="el-icon-upload"
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

<!--    <el-table v-loading="loading" :row-style="rowStyle" :data="flightList" max-height="450px" stripe @selection-change="handleSelectionChange">-->
<!--      <el-table-column type="selection" align="center" />-->
<!--      <el-table-column label="序号" type="index" align="center" width="60">-->
<!--        <template slot-scope="scope">{{(queryParams.pageNum-1)*queryParams.pageSize+scope.$index+1}}</template>-->
<!--      </el-table-column>-->
<!--      <el-table-column label="航班号" align="center" prop="projectCode" width="170px"/>-->
<!--      <el-table-column label="机号" align="center" prop="projectCode" width="170px"/>-->
<!--      <el-table-column label="机龄" align="center" prop="projectCode" width="170px"/>-->
<!--      <el-table-column label="航班状态" align="center" prop="projectCode" width="170px"/>-->
<!--      <el-table-column label="预计起飞时间" align="center" prop="projectCode" width="170px"/>-->
<!--      <el-table-column label="上次检测时间" align="center" prop="projectCode" width="170px"/>-->
<!--      <el-table-column label="健康状况" align="center" prop="projectCode" width="170px"/>-->
<!--      <el-table-column label="操作" align="center" width="130px" fixed="right" class-name="small-padding fixed-width" v-if="columns[18].visible">-->
<!--        <template slot-scope="scope">-->
<!--          <el-button-->
<!--              size="mini"-->
<!--              type="text"-->
<!--              icon="el-icon-edit"-->
<!--              @click="handleUpdate(scope.row)"-->
<!--          >修改</el-button>-->
<!--          <el-button-->
<!--              size="mini"-->
<!--              type="text"-->
<!--              icon="el-icon-delete"-->
<!--              @click="handleDelete(scope.row)"-->
<!--          >删除</el-button>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--    </el-table>-->

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
      loading: true,
      // 航班信息列表
      flightList: [],
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
        flightId: '',
        aircraftId: '',
        terminalId: '',
        healthStatus: '',
        approvalStatus: '',
        estimatedDeparture: '',
        estimatedArrival: '',
        flightStatus: '',
        actualDeparture: '',
        actualArrival: '',
        createdAt: '',
        updatedAt: ''
      }
    }
  }
}
</script>

<style scoped>

</style>