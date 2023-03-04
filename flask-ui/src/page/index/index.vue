<template>
  <el-container class="header-class">
    <el-header
      style="display: flex; background-color: rgb(41, 42, 52); align-items: stretch; justify-content: space-between; height: 50px; padding: 0px 10px; color: rgb(174, 175, 185);">

      <div style="display: flex; align-items:center;">
        <span style="margin-left: 10px; font-size:medium;">XAS Analysis</span>
      </div>

      <div style="display: flex; align-items:center;">
        <div style="vertical-align: middle; margin-top: 30px;margin-right: 28px;">
          <el-dropdown>
            <span>
              <el-avatar :size="34" :src="circleUrl" />
            </span>

            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item divided @click="logout">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>

          </el-dropdown>
        </div>
      </div>
    </el-header>

    <el-container>
      <el-aside>
        <el-col>
          <el-menu active-text-color="#ffd04b" background-color="rgb(52, 56, 68)" border-right="none"
            :default-active="activeIndex" text-color="#fff" router>

            <el-menu-item index="/reports" @click='doActiveIndex("/reports")'>
              <el-icon>
                <Notebook />
              </el-icon>
              <span>Reports</span>
            </el-menu-item>

            <el-menu-item index="/users" @click='doActiveIndex("/users")'>
              <el-icon>
                <UserFilled />
              </el-icon>
              <span>Users</span>
            </el-menu-item>

          </el-menu>
        </el-col>
      </el-aside>

      <el-main>
        <router-view />
      </el-main>

    </el-container>
  </el-container>

</template>

<script>
  import {
    Notebook,
    UserFilled,
  } from '@element-plus/icons-vue'

  export default {
    data() {
      return {
        activeIndex: '',
        circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        logoutInfo: {
          name: "",
        }
      }
    },
    components: {
      Notebook,
      UserFilled,
    },
    created() {
      this.activeIndex = window.sessionStorage.getItem('activeIndex')
      if (!this.activeIndex) {
        this.activeIndex = '/reports'
      }
    },
    methods: {
      logout() {
        this.logoutInfo.name = window.sessionStorage.getItem("account")
        this.$http.post("/user/logout", this.logoutInfo)
          .then((res) => { })
          .catch((err) => { })

        window.sessionStorage.clear()
        // jupm to index page
        this.$router.push('/')
      },
      doActiveIndex(activeIndex) {
        window.sessionStorage.setItem('activeIndex', activeIndex)
        this.activeIndex = activeIndex
      }
    }
  }
</script>

<style scoped="scoped">
  .header-class {
    height: 100%;
    width: 100%;
    font-weight: 400;
    font-style: normal;
    min-width: 1120px;
    z-index: 1002;
    top: 0;
    left: 0;
    background-color: #ebe7e7;
  }

  .el-aside {
    background: rgb(51, 55, 68);
    height: 100%;
    width: 200px;
  }

  .el-header {
    background: rgb(55, 61, 61);
    display: flex;
    justify-content: space-between;
    line-height: 60px;
    color: #fff;
    font-size: 25px;
  }

  .el-main {
    background: #fff;
  }

  .el-menu {
    border-right: none;
    width: 200px;
  }
</style>