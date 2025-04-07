<template>
  <div>
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true" class="query-form">
          <el-form-item label="字典名称" prop="dictName">
            <el-input v-model="queryParams.dictName"
                      placeholder="请输入字典名称"
                      clearable maxlength="50"
                      style="width: 200px;"
                      @keyup.enter.native="handleQuery"/>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
            <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
          </el-form-item>
    </el-form>

    <el-row :gutter="10" style="margin-bottom: 8px">
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
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
            type="danger"
            plain
            icon="el-icon-delete"
            size="mini"
            :disabled="multiple"
            @click="handleDelete"
        >删除</el-button>
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
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns" page-key="dictionary"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="dictList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" width="60">
        <template slot-scope="scope">{{(queryParams.pageNum-1)*queryParams.pageSize+scope.$index+1}}</template>
      </el-table-column>
      <el-table-column label="字典键值" align="center" prop="dictKey" />
      <el-table-column label="字典名称" align="center" prop="dictName" />
      <el-table-column label="字典描述" align="center" prop="description" :show-overflow-tooltip="true"/>
      <el-table-column label="操作" align="center" fixed="right" width="180">
        <template slot-scope="scope">
          <el-button
              size="mini"
              type="text"
              icon="el-icon-edit"
              @click="handleUpdate(scope.row)"
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

<!--    新增/修改弹窗-->
    <el-dialog :title="title" :visible.sync="open" width="520px" append-to-body :close-on-click-modal="false">
      <el-form ref="form" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="字典键值" prop="dictKey">
          <el-input v-model="form.dictKey" placeholder="请输入字典键值" />
        </el-form-item>
        <el-form-item label="字典名称" prop="dictName">
          <el-input v-model="form.dictName" placeholder="请输入字典名称" />
        </el-form-item>
<!--        <el-form-item label="状态" prop="status">-->
<!--          <el-radio-group v-model="form.status">-->
<!--            <el-radio-->
<!--                v-for="dict in dict.type.sys_normal_disable"-->
<!--                :key="dict.value"-->
<!--                :label="dict.value"-->
<!--            >{{dict.label}}</el-radio>-->
<!--          </el-radio-group>-->
<!--        </el-form-item>-->
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "Dictionary",
  data() {
    return {
      // 遮罩层
      loading: false,
      show_status: false,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 3,
      // 字典列表
      dictList: [
        { dictKey: 'terminal_building', dictName: '航站楼', description: '--' },
        { dictKey: 'role_config', dictName: '角色配置', description: '--' },
        { dictKey: 'department', dictName: '部门', description: '--' },
      ],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        dictKey: null,
        dictName: null,
        description: null,
        parentKey: null,
        sortOrder: null,
        createdAt: null,
        updatedAt: null
      },
      // 弹窗标题
      title: '',
      // 弹窗显示
      open: false,
      // 表单
      form: {},
      rules: {
        dictName: [
          { required: true, message: "字典名称不能为空", trigger: "blur" }
        ],
        dictKey: [
          { required: true, message: "字典键值不能为空", trigger: "blur" }
        ]
      },
      columns: []
    }
  },
  created() {
    this.getList();
  },
  methods: {
    getList(){

    },
    handleQuery(){
      this.queryParams.pageNum = 1;
      this.getList();
    },
    resetQuery(){
      this.resetForm("queryForm");
      this.handleQuery();
    },
    handleAdd(){
      this.reset();
      this.open = true;
      this.title = "添加字典";
    },
    handleUpdate(row){
      this.reset();
      const dictId = row.dictId || this.ids
      // getType(dictId).then(response => {
      //   this.form = response.data;
        this.form = row;
        this.open = true;
        this.title = "修改字典类型";
      // });
    },
    /** 提交按钮 */
    submitForm: function() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.dictKey !== undefined) {
            // updateType(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
            //   this.open = false;
            //   this.getList();
            // });
          } else {
            // addType(this.form).then(response => {
              this.$modal.msgSuccess("新增成功");
            //   this.open = false;
            //   this.getList();
            // });
          }
        }
      });
    },
    handleExport(){
      // this.download('system/dict/type/export', {
      //   ...this.queryParams
      // }, `type_${new Date().getTime()}.xlsx`)
    },
    handleDelete(row){
      const dictIds = row.dictId || this.ids;
      // this.$modal.confirm('是否确认删除字典编号为"' + dictIds + '"的数据项？').then(function() {
      //   return delType(dictIds);
      // }).then(() => {
      //   this.getList();
        this.$modal.msgSuccess("删除成功");
      // }).catch(() => {});
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.dictId)
      this.single = (selection.length!==1)
      this.multiple = !selection.length
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        dictId: undefined,
        dictName: undefined,
        dictType: undefined,
        status: "0",
        remark: undefined
      };
      this.resetForm("form");
    },
  }
}
</script>

<style scoped>
.query-form{
  display: flex;
  justify-content: space-between;
}
</style>