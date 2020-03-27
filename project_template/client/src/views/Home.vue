<template>
  <div class="main-content">
    <div class="header-section">
      <div id="user">
        <el-dropdown size="mini" split-button type="primary">
          <span>{{ $store.getters.user }}</span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>
              <span @click="onLogout">注销</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <div class="contentList" id="contentList" v-loading="loading">
      <el-container>
        <el-aside width="200px" style="border-right: 1px solid lightgray;">
          <el-menu
            :default-active="activeMenu"
            @select="changeMenu"
            mode="vertical"
            style="border: unset;"
          >
            <el-menu-item index="history">历史提交记录</el-menu-item>
            <el-menu-item index="upload">添加链接文件</el-menu-item>
            <el-menu-item index="singleLink">添加新链接</el-menu-item>
          </el-menu>
        </el-aside>
        <el-container v-show="activeMenu == 'history'">
          <el-header style="height:60px;margin:20px">
            <div class="search-options">
              <span class="search-label">关键字:</span>
              <el-input placeholder="请输入内容" v-model="searchContent" style="width: unset;"></el-input>

              <span class="search-label" style="margin-left: 10px;">时间范围:</span>
              <el-date-picker
                v-model="searchDateRange"
                type="datetimerange"
                value-format="yyyy-MM-dd HH:mm:ss"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                :default-time="['00:00:00', '23:59:59']"
                :clearable="false"
                @change="getTableData()"
              ></el-date-picker>

              <el-button type="primary" style="margin-left: 10px;" @click="getQueryParams()">搜索</el-button>
              <el-divider></el-divider>
            </div>
          </el-header>
          <el-main>
            <div class="table-data">
              <!-- <el-table ref="multipleTable" :data="tableData" style="width: 100%" @select-all="handleSelectAll" @selection-change="handleSelectionChange"> -->
              <el-table
                ref="multipleTable"
                :data="tableData"
                style="width: 100%"
                stripe
                @sort-change="sortChange"
              >
                <!-- <el-table-column type="selection" width="55"></el-table-column> -->
                <el-table-column type="index" width="50" :index="indexMethod"></el-table-column>
                <el-table-column label="文件名称" width="150" align="center">
                  <template slot-scope="scope">
                    <el-link
                      @click="showXmlList(scope.row.taskId)"
                      style="text-decoration: none;"
                    >{{scope.row.name}}</el-link>
                  </template>
                </el-table-column>
                <el-table-column prop="taskId" label="Task ID" min-width="150" align="center"></el-table-column>
                <el-table-column
                  label="创建时间"
                  prop="created_at"
                  width="200"
                  align="center"
                  sortable="custom"
                ></el-table-column>
                <el-table-column prop="total" label="链接总数" width="80" align="center"></el-table-column>
                <el-table-column prop="success" label="成功总数" width="80" align="center"></el-table-column>
                <el-table-column label="进度" width="175" align="center">
                  <template slot-scope="scope">
                    <div>
                      <el-progress :percentage="scope.row.progress" :color="customColors"></el-progress>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="操作" align="center" width="80">
                  <template slot-scope="scope">
                    <el-button type="danger" size="mini" @click="deleteTask(scope.row.taskId)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>

              <div class="table-pagination">
                <el-pagination
                  layout="total, prev, pager, next"
                  background
                  :total="total"
                  :page-size.sync="pageSize"
                  :current-page.sync="pageNumber"
                  @current-change="getQueryParams"
                ></el-pagination>
              </div>
            </div>

            <el-dialog title="链接详情" :visible.sync="dialogVisible" width="50%" center>
              <el-table :data="urlList" style="width: 100%" stripe>
                <el-table-column type="index" width="50" align="center"></el-table-column>
                <el-table-column label="标题" min-width="250" align="center">
                  <template slot-scope="scope">
                    <a
                      target="_blank"
                      :href="scope.row.url"
                      style="text-decoration: none;"
                    >{{scope.row.title | titleFilter}}</a>
                  </template>
                </el-table-column>
                <el-table-column label="视频状态" min-width="250" align="center">
                  <template slot-scope="scope">
                    <div
                      v-if="scope.row.video_url && scope.row.status >= 0"
                    >{{ scope.row.status | video_handler}}</div>
                    <div v-else>无视频</div>
                  </template>
                </el-table-column>
                <el-table-column label="操作" align="center" width="120">
                  <template slot-scope="scope">
                    <el-button
                      type="primary"
                      size="small"
                      @click="showXmlDetail(scope.row.url)"
                    >在线xml</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialogVisible = false">关闭</el-button>
              </span>
            </el-dialog>
          </el-main>
        </el-container>

        <el-container v-show="activeMenu == 'upload'">
          <el-upload
            class="upload"
            drag
            :action="uploadApi"
            :data="postData"
            :on-success="uploadSuccess"
            :on-error="uploadError"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或
              <em>点击上传</em>
            </div>
            <!-- <div slot="tip" class="el-upload__tip" style="text-align: center;">
              <el-switch
                inactive-text="强制更新"
                v-model="forceUpdate"
                active-color="#13ce66"
                inactive-color="#ff4949"
              ></el-switch>
            </div>-->
            <div slot="tip" class="el-upload__tip">1.只能上传txt文件</div>
            <div slot="tip" class="el-upload__tip">2.链接必须以http或者https开头,要求合法有效</div>
            <div slot="tip" class="el-upload__tip">3.文本文件中的链接必须以换行符分割</div>
          </el-upload>
        </el-container>

        <el-container v-show="activeMenu == 'singleLink'">
          <div class="singleUrl" style="align:center;margin:90px auto;">
            <el-input
              v-model="sigLink"
              placeholder="直接粘贴需要采集的链接"
              @keyup.enter.native="$event.target.blur"
              @blur="postToCrawl"
            >
              <i slot="suffix" class="el-input__icon el-icon-upload" @click="postToCrawl"></i>
            </el-input>
          </div>
        </el-container>
      </el-container>
    </div>
  </div>
</template>

<script>
import moment from "moment";
let Base64 = require("js-base64").Base64;
export default {
  name: "Home",
  data: function() {
    const uploadApi = this.$store.state.url.util.uploadFile;
    return {
      // 菜单项: history || upload
      activeMenu: "history",

      // 关键字
      searchContent: "",
      order: null,

      // 事件范围
      searchDateRange: [
        moment()
          .startOf("day")
          .subtract(1, "D")
          .format("YYYY-MM-DD HH:mm:ss"),
        moment()
          .endOf("day")
          .format("YYYY-MM-DD HH:mm:ss")
      ],

      // 展示列表呐
      tableData: [],

      // 弹窗
      dialogVisible: false,
      urlList: [],

      // 一些分页和辅助功能
      loading: false,
      total: 0,
      pageNumber: 1,
      pageSize: 10,
      uploadApi: uploadApi,
      customColors: [
        { color: "#f56c6c", percentage: 20 },
        { color: "#e6a23c", percentage: 40 },
        { color: "#5cb87a", percentage: 60 },
        { color: "#1989fa", percentage: 80 },
        { color: "#6f7ad3", percentage: 100 }
      ],
      sigLink: "",
      forceUpdate: false
    };
  },
  watch: {
    searchContent(val) {
      this.parametersChanged = true;
    }
  },
  computed: {
    postData() {
      return { switch: this.forceUpdate ? 1 : 0 };
    }
  },
  methods: {
    getQueryParams() {
      this.$store.commit(
        "addInterval",
        setInterval(() => {
          this.getTableData();
        }, 2500)
      );
    },
    onLogout() {
      this.$store.commit("clearToken");
      this.$router.push({ path: "/login" });
    },
    indexMethod(index) {
      return (this.pageNumber - 1) * this.pageSize + index + 1;
    },
    sortChange(column) {
      this.order = column.order;
    },
    getTableData() {
      // 请求数据的时候,先把各个状态初始化一下
      if (this.parametersChanged) {
        // 分页先调一调
        this.pageNumber = 1;

        // 数据也清一清
        // this.tableData = [];
      }
      // this.startLoading();

      // 请求一下数据
      this.$http({
        url: this.$store.state.url.util.historyList,
        method: "get",
        params: {
          searchContent: this.searchContent,
          startTime: String(this.searchDateRange[0]).replace("+", " "),
          endTime: String(this.searchDateRange[1]).replace("+", " "),
          pageNumber: this.pageNumber,
          pageSize: this.pageSize,
          order: this.order
        }
      })
        .then(response => {
          let res = response.data;
          this.stopLoading();
          //待补充
        })
        .catch(e => {
          this.$message.error("获取列表失败!");
        });
    },
    showXmlList(taskId) {
      this.dialogVisible = true;
      // 请求一下数据
      this.$http({
        url: this.$store.state.url.util.xmlList,
        method: "get",
        params: {
          taskId: taskId
        }
      })
        .then(response => {
          let res = response.data;
          this.stopLoading();
          //待补充
        })
        .catch(e => {
          this.$message.error("获取详情失败!");
        });
    },
    deleteTask(taskId) {
      this.$http({
        url: this.$store.state.url.util.delete,
        method: "post",
        data: {
          taskId: taskId,
          searchContent: this.searchContent,
          startTime: String(this.searchDateRange[0]).replace("+", " "),
          endTime: String(this.searchDateRange[1]).replace("+", " "),
          pageNumber: this.pageNumber,
          pageSize: this.pageSize
        }
      })
        .then(response => {
          let res = response.data;
          this.stopLoading();
          //待补充
        })
        .catch(e => {
          this.$message.error("获取详情失败!");
        });
    },
    showXmlDetail(url) {
      window.open(
        this.$store.state.url.util.onlineXmlDetail +
          "?url=" +
          Base64.encode(url),
        "_blank"
      );
    },
    changeMenu(menuIndex = "history") {
      this.sigLink = "";
      if (menuIndex != "history") {
        this.$store.commit("clearIntervals");
      }
      this.activeMenu = menuIndex;
    },
    uploadError(err, file, fileList) {
      this.$message({ message: "上传失败", type: "error" });
    },
    uploadSuccess(response, file, fileList) {
      if (response.status == 1) {
        this.$message({ message: "上传成功!", type: "success" });
        this.activeMenu = "history";
        this.getQueryParams();
      } else {
        this.$message({
          message: "上传失败:" + response.message,
          type: "error"
        });
      }
    },
    startLoading() {
      this.loading = true;
    },
    stopLoading() {
      this.loading = false;
    },
    postToCrawl() {
      if (this.sigLink.trim() == "") {
        this.$message({ message: "链接不能为空！", type: "error" });
        return;
      }
      this.$http({
        url: this.$store.state.url.util.uploadLink,
        method: "post",
        data: {
          singleLink: this.sigLink
        }
      })
        .then(response => {
          let res = response.data;
          this.stopLoading();
          if (res.status == 1) {
            this.$message({ message: "上传成功!", type: "success" });
            this.activeMenu = "history";
            this.getQueryParams();
          } else {
            this.$message({
              message: "上传失败:" + response.message,
              type: "error"
            });
          }
        })
        .catch(e => {
          this.$message.error("获取详情失败!");
        });
    }
  },
  created() {
    this.getQueryParams();
  },
  filters: {
    titleFilter(value) {
      return value.length <= 15 ? value : value.slice(0, 15) + "...";
    },
    handleDate(value) {
      return value.split(".")[0];
    },
    video_handler(value) {
      const video_status_hander = [
        "未抓取",
        "已完成",
        "抓取中",
        "抓取失败",
        "上传中",
        "上传失败",
        "视频云处理中",
        "xml生成中"
      ];
      return video_status_hander[value];
    }
  }
};
</script>

<style lang="scss">
.main-content {
  margin: auto 5%;
}

.main-content .header-section {
  float: right;
  height: 20px;
}

#user {
  padding-top: 15px;
  padding-right: 15px;
  .el-button {
    margin: 0 !important;
    border-right: none;
  }
  // .el-button--primary {
  //   color: #ffffff;
  //   background-color: #35cbaa;
  //   border-color: #35cbaa;
  // }
}

.el-menu-item {
  border-bottom: 1px solid #eee;
  width: 96%;
  margin: 0 auto;
  text-align: center;
}

.top-bar {
  background-color: #00477f;
  padding: 10px;
  padding-top: 17px;
}

.top-bar img {
  height: 40px;
}

.singleUrl .el-input {
  min-width: 500px;
}

.contentList {
  padding-top: 55px;
}

.el-switch__label .is-active {
  color: lightgray;
}

.contentList .el-container {
  min-height: 500px;
  border: 1px solid rgb(238, 238, 238);
}

// .search-bar {
//   width: 50%;
//   margin: 40px auto;
// }

// .search-bar input.el-input__inner {
//   border-color: #00477f;
//   height: 46px;
//   border-top-left-radius: 7px;
//   border-bottom-left-radius: 7px;
// }

// .search-bar i.el-icon-search {
//   color: #fff;
//   font-size: 20px;
// }

span.search-label {
  font-size: 15px;
  padding-right: 10px;
  /* margin-left: 10px;
  margin-right: 10px; */
}

.search-options {
  text-align: center;
  vertical-align: 15px;
}

.search-options .el-divider.el-divider--horizontal {
  background-color: black;
}

.search-options input.el-input__inner {
  width: 150px;
}

.table-item-title {
  margin: 8px 0;
}

.table-item-title span.el-link--inner {
  font-size: 16px;
  color: #04477f;
  font-weight: bold;
}

.table-item-info span {
  margin-right: 30px;
}

.table-pagination {
  margin-top: 25px;
  text-align: center;
  margin-bottom: 5vh;
}

.table-pagination
  .el-pagination.is-background
  .el-pager
  li:not(.disabled).active {
  background-color: #003366;
  color: #fff;
  border-radius: 4px;
}

.el-checkbox-group span.el-checkbox__label {
  display: none;
}

/* 导出功能相关 */
#toExportExcel {
  display: none;
}

.upload {
  margin: auto;
}
</style>