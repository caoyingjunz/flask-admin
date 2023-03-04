<template>
    <div>
        <el-breadcrumb separator="/">
            <el-breadcrumb-item>
                <span style="font-weight: bold; font-size: 18px; color: black;">Users</span>
            </el-breadcrumb-item>
        </el-breadcrumb>

        <div style="margin-top: 30px;">
            <el-row :gutter="40">
                <el-col :span="6">
                    <el-button type="primary" @click="createUser">
                        <el-icon style="vertical-align: middle;margin-right: 8px;">
                            <plus />
                        </el-icon> New User
                    </el-button>
                    <el-button @click="getUserList" type="primary" plain>
                        <el-icon style="vertical-align: middle;margin-right: 4px; ">
                            <refresh />
                        </el-icon> Refresh
                    </el-button>
                </el-col>
            </el-row>

            <el-table :data="userList" stripe style="margin-top: 20px; width: 100%" v-loading="loading">
                <el-table-column prop="id" label="UserId" width="110" sortable />
                <el-table-column prop="name" label="Name" width="180" />
                <el-table-column prop="email" label="Email" width="200" />
                <el-table-column prop="description" label="Description" />
                <el-table-column fixed="right" label="Actions" width="260">
                    <template #default="scope">
                        <el-button type="primary" plain size="small" @click="handleUserEdit(scope.row)">
                            <el-icon style="vertical-align: middle; margin-right: 5px;">
                                <Edit />
                            </el-icon> Edit
                        </el-button>

                        <el-button type="success" plain size="small" @click="handleChangePassword(scope.row)"
                            style="margin-left: 10px">
                            <el-icon style="vertical-align: middle;margin-right: 5px;">
                                <Switch />
                            </el-icon> Change Password
                        </el-button>
                    </template>
                </el-table-column>

                <template v-slot:empty>
                    <div>no user data</div>
                </template>

            </el-table>
        </div>

        <el-dialog v-model="createUserDialogFormVisible" title="New User" width="40%" draggable
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
                    <el-input v-model="createUserForm.confirm_password" placeholder="Input password again"
                        show-password />
                </el-form-item>

                <el-form-item label="Email" prop="email">
                    <el-input v-model="createUserForm.email"
                        placeholder="Input Email, format: <email_name>@gmail.com" />
                </el-form-item>

                <el-form-item label="description" prop="description">
                    <el-input v-model="createUserForm.description" placeholder="Please input description"
                        type="textarea" :autosize="autosize" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="cancelUserCreate">Cancel</el-button>
                    <el-button type="primary" @click="confirmUserCreate">Confirm</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="editDialogFormVisible" title="Edit User" width="40%" draggable @close="editDialogClose">
            <el-form ref="editUserFormRef" :model="editUserForm" :rules="editUserFormRules" label-width="120px"
                label-position="top">

                <el-form-item label="UserId" prop="id">
                    <el-input v-model="editUserForm.id" disabled />
                </el-form-item>

                <el-form-item label="Name" prop="name">
                    <el-input v-model="editUserForm.name" disabled />
                </el-form-item>

                <el-form-item label="Emal" prop="email">
                    <el-input v-model="editUserForm.email" placeholder="Please input email" />
                </el-form-item>

                <el-form-item label="Description" prop="description">
                    <el-input v-model="editUserForm.description" type="textarea" :autosize="autosize" />
                </el-form-item>

            </el-form>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="cancelEditUser">Cancel</el-button>
                    <el-button type="primary" @click="confirmEditUser">Confirm</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="changePasswordDialogFormVisible" title="Change Password" width="40%" draggable
            @close="changePasswordClose">
            <el-form :model="changePassword" label-width="120px" label-position="top">
                <el-form-item label="UserId" prop="id">
                    <el-input v-model="changePassword.user_id" disabled />
                </el-form-item>
                <el-form-item label="Original Password" prop="old_password">
                    <el-input v-model="changePassword.old_password" type="password" clearable />
                </el-form-item>
                <el-form-item label="Password" prop="password">
                    <el-input v-model="changePassword.password" type="password" clearable />
                </el-form-item>
                <el-form-item label="Confirm Password" prop="confirm_password">
                    <el-input v-model="changePassword.confirm_password" type="password" clearable />
                </el-form-item>
            </el-form>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="cancelChangeword2">Cancel</el-button>
                    <el-button type="primary" @click="confirmChangeword">Confirm</el-button>
                </span>
            </template>
        </el-dialog>

    </div>
</template>

<script>
    import {
        Refresh,
        Edit,
        Switch,
        Plus
    } from '@element-plus/icons-vue'

    export default {
        data() {
            return {
                loading: false,
                createUserDialogFormVisible: false,
                editDialogFormVisible: false,
                changePasswordDialogFormVisible: false,
                autosize: {
                    minRows: 4,
                },
                userList: [],
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
                editUserForm: {
                    id: 0,
                    name: '',
                    email: '',
                    description: '',
                },
                changePassword: {
                    user_id: '',
                    old_password: '',
                    password: '',
                    confirm_password: '',
                },
                editUserFormRules: {}
            }
        },
        created() {
            this.getUserList()
        },
        methods: {
            async getUserList() {
                this.loading = true

                const user_name = window.sessionStorage.getItem('account')
                const {
                    data: res
                } = await this.$http.get('/user/list?user_name=' + user_name, {
                    params: this.userInfo
                })

                this.loading = false
                if (res.code != 200) {
                    return this.$message.error('failed to get user list');
                }
                this.userList = res.result
            },
            createUser() {
                this.createUserDialogFormVisible = true
            },
            confirmUserCreate() {
                this.createUserDialogFormVisible = false
                this.$http.post("/user/register", this.createUserForm)
                    .then((res) => {
                        this.getUserList()
                        return this.$message.success(this.createUserForm.name + " register success")
                    })
                    .catch((err) => {
                        return this.$message.error(err.toString())
                    })
            },
            cancelUserCreate() {
                this.createUserDialogFormVisible = false
            },
            createUserDialogClose() {
                this.$refs.createUserFormRef.resetFields()
            },
            handleUserEdit(row) {
                this.editUserForm.id = row.id
                this.editUserForm.name = row.name
                this.editUserForm.email = row.email
                this.editUserForm.description = row.description

                this.editDialogFormVisible = true
            },
            handleChangePassword(row) {
                this.changePassword.user_id = row.id
                this.changePasswordDialogFormVisible = true
            },
            confirmEditUser() {
                this.editDialogFormVisible = false

                this.$http.put("/user/update", this.editUserForm)
                    .then((res) => {
                        this.getUserList()
                        return this.$message.success(this.editUserForm.user_id + " edit success")
                    })
                    .catch((err) => {
                        return this.$message.error(err.toString())
                    })
            },
            cancelEditUser() {
                this.editDialogFormVisible = false
            },
            editDialogClose() {
                this.$refs.editUserFormRef.resetFields()
            },
            cancelChangeword2() {
                this.changePasswordClose()
                this.changePasswordDialogFormVisible = false
            },
            changePasswordClose() {
                this.changePassword.old_password = ''
                this.changePassword.password = ''
                this.changePassword.confirm_password = ''
            },
            confirmChangeword() {
                if (this.changePassword.old_password == '') {
                    return this.$message.error("invaild empty original password")
                }
                if (this.changePassword.password == '') {
                    return this.$message.error("invaild empty password")
                }
                if (this.changePassword.confirm_password == '') {
                    return this.$message.error("invaild empty confirm password")
                }
                if (this.changePassword.confirm_password != this.changePassword.password) {
                    return this.$message.error("password different from confirm password")
                }
                if (this.changePassword.password == this.changePassword.old_password) {
                    return this.$message.error("password equal to original password")
                }

                this.$http.post("/user/password", this.changePassword)
                    .then((res) => {
                        const data = res.data
                        if (data.code != 200) {
                            return this.$message.error(data.message)
                        }

                        this.changePasswordClose()
                        this.getUserList()
                        this.changePasswordDialogFormVisible = false
                        return this.$message.success("change password success")
                    })
                    .catch((err) => {
                        return this.$message.error("change password failed")
                    })
            },
            async handleUserDelete(row) {
                this.$confirm('Proxy will permanently delete the file. Continue?', {
                        confirmButtonText: 'OK',
                        cancelButtonText: 'Cancel',
                        type: 'warning',
                        draggable: true,
                    })
                    .then(() => {
                        this.$http.delete("/user/delete?user_id=" + row.id)
                            .then((res) => {
                                this.getUserList()
                                return this.$message.success(row.name + " 删除成功")
                            })
                            .catch((err) => {
                                return this.$message.error(err.toString())
                            })
                    })
                    .catch(() => {
                    })
            },
        },
        components: {
            Switch,
            Edit,
            Plus,
            Refresh
        }
    }
</script>