<template>
  <div class="top-right-btn" :style="style">
    <el-row>
      <el-tooltip class="item" effect="dark" :content="showSearch ? '隐藏搜索' : '显示搜索'" placement="top" v-if="search">
        <el-button size="mini" circle icon="el-icon-search" @click="toggleSearch()" />
      </el-tooltip>
      <el-tooltip class="item" effect="dark" content="刷新" placement="top">
        <el-button size="mini" circle icon="el-icon-refresh" @click="refresh()" />
      </el-tooltip>
      <el-tooltip class="item" effect="dark" content="显隐列" placement="top" v-if="columns">
        <el-button size="mini" circle icon="el-icon-menu" @click="showColumn()" v-if="showColumnsType == 'transfer'"/>
        <el-dropdown trigger="click" :hide-on-click="false" style="padding-left: 12px" v-if="showColumnsType == 'checkbox'">
          <el-button size="mini" circle icon="el-icon-menu" />
          <el-dropdown-menu slot="dropdown" style="max-height: 600px; overflow: auto">
            <template v-for="item in columns">
              <el-dropdown-item :key="item.key">
                <el-checkbox :checked="item.visible" @change="checkboxChange($event, item.label)" :label="item.label" />
              </el-dropdown-item>
            </template>
          </el-dropdown-menu>
        </el-dropdown>
      </el-tooltip>
    </el-row>
    <el-dialog :title="title" :visible.sync="open" append-to-body>
      <el-transfer
          :titles="['显示', '隐藏']"
          v-model="value"
          :data="columns"
          @change="dataChange"
      ></el-transfer>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: "RightToolbar",
  data() {
    return {
      // 显隐数据
      value: [],
      // 弹出层标题
      title: "显示/隐藏",
      // 是否显示弹出层
      open: false,
    };
  },
  props: {
    /* 是否显示检索条件 */
    showSearch: {
      type: Boolean,
      default: true,
    },
    /* 显隐列信息 */
    columns: {
      type: Array,
    },
    /* 是否显示检索图标 */
    search: {
      type: Boolean,
      default: true,
    },
    /* 显隐列类型（transfer穿梭框、checkbox复选框） */
    showColumnsType: {
      type: String,
      default: "checkbox",
    },
    /* 右外边距 */
    gutter: {
      type: Number,
      default: 10,
    },
    pageKey: {
      type: String,
      required: true,
    },
  },
  computed: {
    style() {
      const ret = {};
      if (this.gutter) {
        ret.marginRight = `${this.gutter / 2}px`;
      }
      return ret;
    }
  },
  created() {
    this.restoreColumns();
    if (this.showColumnsType === 'transfer') {
      // 显隐列初始默认隐藏列
      for (let item in this.columns) {
        if (this.columns[item].visible === false) {
          this.value.push(parseInt(item));
        }
      }
    }
  },
  methods: {
    // 搜索
    toggleSearch() {
      this.$emit("update:showSearch", !this.showSearch);
    },
    // 刷新
    refresh() {
      this.$emit("queryTable");
    },
    // 右侧列表元素变化
    dataChange(data) {
      for (let item in this.columns) {
        const key = this.columns[item].key;
        this.columns[item].visible = !data.includes(key);
      }
    },
    // 打开显隐列dialog
    showColumn() {
      this.open = true;
    },
    // 勾选
    checkboxChange(event, label) {
      this.columns.filter(item => item.label == label)[0].visible = event;
      this.saveColumns()
    },
    saveColumns() {
      // reduce：{ key: 0, label: `账单编号`, visible: true } ==> 0：true
      const columnVisibility = this.columns.reduce((acc, column) => {
        acc[column.key] = column.visible;
        return acc;
      }, {});
      // 存储到浏览器本地缓存
      localStorage.setItem(`columnVisibility_${this.pageKey}`, JSON.stringify(columnVisibility));
    },
    restoreColumns() {
      // 读取浏览器缓存
      const savedVisibility = localStorage.getItem(`columnVisibility_${this.pageKey}`);
      // 修改column每个key相应的visible
      if (savedVisibility) {
        const columnVisibility = JSON.parse(savedVisibility);
        this.columns.forEach(column => {
          if (columnVisibility.hasOwnProperty(column.key)) {
            column.visible = columnVisibility[column.key];
          }
        });
      }
    }
  },
};
</script>
<style scoped>
::v-deep .el-transfer__button {
  border-radius: 50%;
  padding: 12px;
  display: block;
  margin-left: 0px;
}
::v-deep .el-transfer__button:first-child {
  margin-bottom: 10px;
}
.top-right-btn {
  position: relative;
  float: right;
}
</style>
