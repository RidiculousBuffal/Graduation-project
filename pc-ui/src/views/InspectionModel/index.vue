<template>
  <div>
    <el-form :model="queryParams" v-show="showSearch" ref="queryForm" size="small" :inline="true">
      <el-form-item label="检测模型名称" prop="modelId">
        <el-select v-model="queryParams.modelId"
                  placeholder="请输入检测模型名称"
                  clearable maxlength="50"
                  style="width: 200px;"
                  @change="handleQuery">
          <el-option v-for="item in modelList" :key="item.modelId"
                     :value="item.modelId" :label="item.modelName" ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button
            type="info"
            plain
            size="mini"
            @click="handleViewModelImage">查看本模型图</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" style="margin-bottom: 8px">
      <el-col :span="1.5">
        <el-button
            type="primary"
            plain
            icon="el-icon-plus"
            size="mini"
            @click="handleAddModel"
        >新增模型</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
            type="primary"
            plain
            icon="el-icon-plus"
            size="mini"
            @click="handleAddProject"
        >新增项目</el-button>
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
      <el-table-column label="检测项目编号" align="center" prop="projectId" />
      <el-table-column label="检测项目名称" align="center" prop="projectName" />
      <el-table-column label="项目点位" align="center" prop="projectPoints" />
      <el-table-column label="描述" align="center" prop="description" />
      <el-table-column label="标记情况" align="center" prop="tagStatus" width="100px">
        <template slot-scope="scope">
          <div :style="{borderRadius: '5px', backgroundColor: getTagBackColor(scope.row.tagStatus), color: getTagNameBackColor(scope.row.tagStatus)}">
            {{ Boolean(scope.row.tagStatus) ? '是' : '否' }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="示意图" align="center" prop="referenceImages" />
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
          <el-button
              size="mini"
              type="text"
              icon="el-icon-edit"
              @click="handleTag(scope.row)"
          >标记点位</el-button>
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

    <!--    新增模型弹窗-->
    <el-dialog title="新增模型" :visible.sync="modalOpen" width="520px" append-to-body :close-on-click-modal="false">
      <el-form ref="modelForm" :model="modelForm" :rules="rules" label-width="90px">
        <el-form-item label="模型名称" prop="modalName">
          <el-input v-model="modelForm.modalName" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="对应机型" prop="modelAircraftTypeId">
          <el-select v-model="modelForm.modelAircraftTypeId" placeholder="请选择对应飞机型号">
            <el-option v-for="item in aircraftTypeList" :key="item.typeId"
                       :value="item.typeId" :label="item.typeName"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="modelDescription">
          <el-input v-model="modelForm.modelDescription" type="textarea" placeholder="请输入内容"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitModelForm">确 定</el-button>
        <el-button @click="cancelAddModel">取 消</el-button>
      </div>
    </el-dialog>
    <!--    新增/修改弹窗-->
    <el-dialog :title="title" :visible.sync="open" width="520px" append-to-body :close-on-click-modal="false">
      <el-form ref="form" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="检测项目编号" prop="projectId">
          <el-input v-model="form.projectId" placeholder="请输入检测项目编号" />
        </el-form-item>
        <el-form-item label="检测项目名称" prop="projectName">
          <el-input v-model="form.projectName" placeholder="请输入检测项目名称" />
        </el-form-item>
        <el-form-item label="项目点位" prop="projectPoints">
          <el-input v-model="form.projectPoints" placeholder="请输入项目点位"/>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容"/>
        </el-form-item>
        <el-form-item label="示意图" prop="referenceImages">
          <el-input v-model="form.referenceImages"/>
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
  name: "InspectionModel",
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
        { projectId: '检测项目-1', projectName: '应急设备检查', projectPoints: '1', description: 'xxx', tagStatus: '1', referenceImages: ''},
        { projectId: '检测项目-2', projectName: '起落架系统', projectPoints: '2', description: 'xxx', tagStatus: '0', referenceImages: ''},
        { projectId: '检测项目-3', projectName: '驾驶舱面板', projectPoints: '3', description: 'xxx', tagStatus: '1', referenceImages: ''},
        { projectId: '检测项目-4', projectName: '发动机系统', projectPoints: '4', description: 'xxx', tagStatus: '0', referenceImages: ''},
      ],
      //
      modelList: [],
      //
      aircraftTypeList: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        modelId: null,
      },
      modalOpen:false,
      modelForm: {},
      modelRules: {
        modalName: [
          { required: true, message: "模型名称不能为空", trigger: "blur" }
        ],
        modelAircraftTypeId: [
          { required: true, message: "对应机型不能为空", trigger: "blur" }
        ]
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
    handleViewModelImage(){

    },
    handleAddModel(){
      this.resetModelForm();
      this.modalOpen = true;
      this.title = "添加模型";
    },
    submitModelForm(){
      this.$refs["form"].validate(valid => {
        if (valid) {
          // addType(this.form).then(response => {
          this.$modal.msgSuccess("新增模型成功");
          //   this.open = false;
          //   this.getList();
          // });
        }
      });
    },
    cancelAddModel(){
      this.modalOpen = false;
      this.resetModelForm();
    },
    handleAddProject(){
      this.reset();
      this.open = true;
      this.title = "添加项目";
    },
    handleUpdate(row){
      this.reset();
      const dictId = row.dictId || this.ids
      // getType(dictId).then(response => {
      //   this.form = response.data;
      this.form = row;
      this.open = true;
      this.title = "修改项目";
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
    // 表单重置
    resetModelForm() {
      this.modelForm = {
        modelId: undefined,
        modelName: undefined,
        modelAircraftTypeId: undefined,
        modelDescription: undefined
      };
      this.resetForm("modelForm");
    },
    //
    handleTag(){

    },
    //
    getTagBackColor(tagStatus){
      switch (tagStatus) {
        case '0':
          return '#FFCCCC';
        case '1':
          return '#CCFFCC';
      }
    },
    //
    getTagNameBackColor(tagStatus){
      switch (tagStatus) {
        case '0':
          return '#FF0033';
        case '1':
          return '#009933';
      }
    }
  }
}
</script>

<style scoped>
.query-form{
  display: flex;
  justify-content: space-between;
}
</style>