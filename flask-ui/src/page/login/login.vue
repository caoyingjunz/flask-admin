<template>
    <div class="login_body_Page_Class">
        <div class="login_form_body_Page_Class">
            <div class="login_cont_body_Page_Class">
                <div class="login_container_Page_Class">
                    <div class="login_container_Page_Class">
                        <div class="login_container_form_Page_Class">
                            <div class="login_login_form_Page_Class">
                                <div class="login_form_Page_Class">
                                    <div direction="vertical" class="u-linear-layout_FaugwXHe" gap="large">
                                        <div class="u-tabs_3_DeFFee">
                                            <ul class="u-tabs_head_3_DeFFee">
                                                <li title="User Login" selected="selected" class="u-tabs_item_3_DeFFee">
                                                    <span>User Login</span>
                                                </li>
                                            </ul>
                                        </div>
                                        <el-input v-model="loginInfo.name" :prefix-icon="UserFilled"
                                            placeholder="Input user" clearable maxlength="128"
                                            @keyup.enter.native="login">
                                            <template #prefix>
                                                <el-icon class="el-input__icon">
                                                    <user-filled />
                                                </el-icon>
                                            </template>
                                        </el-input>

                                        <el-input v-model="loginInfo.password" :prefix-icon="Lock"
                                            placeholder="Input password" show-password clearable maxlength="128"
                                            @keyup.enter.native="login">
                                            <template #prefix>
                                                <el-icon class="el-input__icon">
                                                    <lock />
                                                </el-icon>
                                            </template>
                                        </el-input>

                                        <div direction="horizontal" class="u-linear-layout_FaugwXHe" type="flex"
                                            style="position: relative;">
                                            <el-button class="u-button_Forget" type="text" @click="registerUser">
                                                register
                                            </el-button>
                                        </div>

                                        <div direction="horizontal" class="u-linear-layout_FaugwXHe" type="flex"
                                            justify="center">
                                            <a target="_self" class="u-button_IeaEDOvW" color="primary" size="large"
                                                :loading="load" @click="login"> login </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 注册用户对话框区域 -->
    <el-dialog v-model="createUserDialogFormVisible" title="Register User" width="40%" draggable
        @close="createUserDialogClose">
        <el-form ref="createUserFormRef" :model="createUserForm" :rules="createUserFormRules" label-width="10px"
            label-position="top">
            <el-form-item label="Name" prop="name">
                <el-input v-model="createUserForm.name" placeholder="Input user name" />
            </el-form-item>

            <el-form-item label="Password" prop="password">
                <el-input v-model="createUserForm.password" placeholder="Input password" show-password />
            </el-form-item>

            <el-form-item label="ConfirmPassword" prop="confirm_password">
                <el-input v-model="createUserForm.confirm_password" placeholder="Input password again" show-password />
            </el-form-item>

            <el-form-item label="Email" prop="email">
                <el-input v-model="createUserForm.email" placeholder="Input Email" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="cancelUserCreate">Cancel</el-button>
                <el-button type="primary" @click="confirmUserCreate">Confirm</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
    import {
        UserFilled,
        Lock
    } from '@element-plus/icons-vue'

    export default {
        data() {
            return {
                loginInfo: {
                    name: "",
                    password: "",
                },
                load: false,
                createUserDialogFormVisible: false,
                createUserForm: {
                    name: '',
                    password: '',
                    confirm_password: '',
                    email: '',
                    description: '',
                },
                createUserFormRules: {
                    name: [{
                        required: true,
                        message: 'please input user name',
                        trigger: 'blur'
                    }],
                    password: [{
                        required: true,
                        message: 'please input user password',
                        trigger: 'blur'
                    }],
                    confirm_password: [{
                        required: true,
                        message: 'please input user name again',
                        trigger: 'blur'
                    }],
                    description: [{
                        required: false,
                        message: 'please input user description',
                        trigger: 'blur'
                    }],
                },
                Lock: '',
                UserFilled: ''
            }
        },
        methods: {
            registerUser() {
                this.createUserDialogFormVisible = true
            },
            confirmUserCreate() {
                this.createUserDialogFormVisible = false
                this.$http.post("/user/register", this.createUserForm)
                    .then((res) => {
                        this.$refs.createUserFormRef.resetFields()
                        return this.$message.success(this.createUserForm.name + " register success")
                    })
                    .catch((err) => {
                        return this.$message.error(err.toString())
                    })
            },
            cancelUserCreate() {
                this.createUserDialogFormVisible = false
                this.$refs.createUserFormRef.resetFields()
            },

            async login() {
                this.load = true

                this.$http.post("/user/login", this.loginInfo)
                    .then((res) => {
                        const data = res.data
                        if (data.code != 200) {
                            this.load = false
                            return this.$message.error(data.message)
                        }

                        const token = data.result
                        window.sessionStorage.setItem("token", token)
                        window.sessionStorage.setItem("account", this.loginInfo.name)

                        this.$message.success("login success")
                        this.$router.push('/reports')
                    })
                    .catch((err) => {
                        this.load = false
                        return this.$message.error("login failed")
                    })
            },
        },
        components: {
            Lock,
            UserFilled
        }
    }
</script>

<style>
    .u-button_Forget {
        margin: 0;
        overflow: visible;
        font: inherit;
        color: #6383dd;
        position: absolute;
        right: 0px;
        padding: 0px 0px 12px;
    }


    .u-button_IeaEDOvW {
        margin: 0;
        border: none;
        overflow: visible;
        -webkit-appearance: none;
        display: inline-block;
        text-align: center;
        padding: 0 12px;
        font: inherit;
        text-transform: none;
        text-decoration: none;
        cursor: pointer;
        height: 36px;
        width: 3000px;
        line-height: 34px;
        border: 1px solid #e5e8ee;
    }

    .el-input__inner {
        border: 0px solid #dfe4ec;
        height: 40px;
    }


    .u-button_IeaEDOvW[color=primary] {
        background: #508ae4;
        border: none;
        line-height: 34px;
        color: #fff;
    }

    .u-tabs_item_3_DeFFee {
        cursor: pointer;
        display: inline-block;
        padding: 0 20px;
        box-sizing: content-box;
        height: 30px;
        line-height: 30px;
        border: 1px solid transparent;
        border-bottom: none;
        margin-bottom: -1px;
    }

    .u-tabs_item_3_DeFFee[selected] {
        background: #fff;
        border-color: #e0e6ec;
        color: #508ae1;
        border-top: 2px solid #508ae1;
    }

    .u-tabs_head_3_DeFFee {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        height: 30px;
        border-bottom: 1px solid #dfdcdc;
    }

    .u-linear-layout_FaugwXHe[direction=vertical][gap=large]>:not(:last-child) {
        margin-bottom: 30px;
    }

    .u-linear-layout_FaugwXHe[type=flex] {
        display: flex;
        text-align: inherit;
    }

    .login_form_Page_Class {
        width: 325px;
        margin: 0 auto;
        padding: 0;
        line-height: 1;
    }

    .login_login_form_Page_Class {
        float: none;
        width: 450px;
        height: 380px;
        margin: auto;
        padding-top: 30px;
        box-sizing: border-box;
        background: #fff;
        transition: box-shadow .2s;
        box-shadow: 0 0 10px 0 rgb(80 90 109 / 16%);
    }

    .login_container_Page_Class {
        display: table;
        background: transparent;
        width: 1160px;
        margin: 0 auto;
        padding-top: 26px;
    }

    .login_form_body_Page_Class {
        background: none;
        margin: 0;
        padding: 0;
        padding-top: 150px;
    }

    .login_body_Page_Class {
        position: relative;
        box-sizing: border-box;
        padding-bottom: 133px;
        min-height: 100vh;
        background: url(../../../static/beijing.jpg) no-repeat;
        background-size: cover;
    }

    .u-head_head_yingjun {
        width: 100%;
        min-width: 100px;
        height: 65px;
        margin: 0 1px;
        background-color: #eaedf3;
        box-shadow: 0 2px 4px -1px rgb(0 0 0 / 20%), 0 4px 6px 0 rgb(0 0 0 / 15%);
        position: fixed;
        z-index: 1000;
    }

    .u-head_logo_yingjun {
        margin-left: 10px;
        margin-right: 50px;
        display: inline-block;
        height: 65px;
    }
</style>