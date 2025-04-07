<template>
  <div>
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-row>
        <el-col :span="8">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="queryParams.name"
                      placeholder="请输入姓名"
                      clearable maxlength="50"
                      style="width: 200px;"
                      @keyup.enter.native="handleQuery"/>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="工号" prop="engineerId">
            <el-input v-model="queryParams.engineerId"
                      placeholder="请输入工号"
                      clearable maxlength="50"
                      style="width: 200px;"
                      @keyup.enter.native="handleQuery"/>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item style="position: absolute; right: 1%">
            <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
            <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
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
            type="warning"
            plain
            icon="el-icon-download"
            size="mini"
            @click="handleExport"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns" page-key="engineer"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="dictList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" width="60">
        <template slot-scope="scope">{{(queryParams.pageNum-1)*queryParams.pageSize+scope.$index+1}}</template>
      </el-table-column>
      <el-table-column label="工号" align="center" prop="engineerId" />
      <el-table-column label="姓名" align="center" prop="name" />
      <el-table-column label="性别" align="center" prop="gender" />
      <el-table-column label="所属部门" align="center" prop="department" />
      <el-table-column label="工龄" align="center" prop="workYear"/>
      <el-table-column label="人脸图片" align="center" prop="faceInfo" />
      <el-table-column label="联系方式" align="center" prop="contactInfo" />
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
        <el-form-item label="工号" prop="engineerId">
          <el-input v-model="form.engineerId" placeholder="请输入工号" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="性别" prop="description">
          <el-select v-model="form.description" placeholder="请选择性别">
            <el-option v-for="item in genderList" :key="item.dictKey"
                       :value="item.dictKey" :label="item.dictName"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门" prop="department">
          <el-select v-model="form.department" placeholder="请选择所属部门">
            <el-option v-for="item in departmentList" :key="item.dictKey"
                       :value="item.dictKey" :label="item.dictName"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="人脸图片" prop="faceInfo">
          <el-input v-model="form.faceInfo"/>
        </el-form-item>
        <el-form-item label="联系方式" prop="contactInfo">
          <el-input v-model="form.contactInfo" placeholder="请输入联系方式" />
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
  name: "DetectModel",
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
        { engineerId: '33467', name: 'xxx', gender: '女', department: '维修控制中心', faceInfo: '', contactInfo: '13323456472', workYear: '3年'},
        { engineerId: '33468', name: 'admin', gender: '男', department: '航班维修部门', faceInfo: '', contactInfo: '13323456472', workYear: '3年'},
        { engineerId: '33469', name: 'aaa', gender: '女', department: '航班维修部门', faceInfo: '', contactInfo: '13323456472', workYear: '2年'},
        { engineerId: '33470', name: 'bbb', gender: '男', department: '维修控制中心', faceInfo: '', contactInfo: '13323456472', workYear: '1年'},
      ],
      //
      genderList: [],
      //
      departmentList: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        engineerId: null,
        name: null,
        gender: null,
        department: null,
        workYear: null,
        contactInfo: null,
        userId: null,
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