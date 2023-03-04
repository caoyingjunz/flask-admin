<template>
    <div>
        <el-breadcrumb separator="/">
            <el-breadcrumb-item>
                <span style="font-weight: bold; font-size: 18px; color: black;">Reports</span>
            </el-breadcrumb-item>
        </el-breadcrumb>

        <div style="margin-top: 30px;">
            <el-row>
                <el-col>
                    <div>
                        <el-button @click="getReportList" type="primary">
                            <el-icon style="vertical-align: middle;margin-right: 4px; ">
                                <refresh />
                            </el-icon> Refresh
                        </el-button>

                        <el-button type="primary" @click="handleCreate" style="float: right; margin-right: 32px;" plain>
                            <el-icon style="vertical-align: middle;margin-right: 8px;">
                                <upload-filled />
                            </el-icon> Upload XAS
                        </el-button>
                    </div>
                </el-col>
            </el-row>

            <el-table :data="bookList" stripe style="margin-top: 30px; width: 100%" v-loading="loading"
                @selection-change="handleSelectionChange">
                <el-table-column prop="id" label="ReportID" width="120" sortable />
                <el-table-column prop="name" label="ReportName" width="340">
                    <template #default="scope">
                        <el-link type="primary" @click="previewOnLine(scope.row.id)"> {{ scope.row.name }} </el-link>
                    </template>
                </el-table-column>
                <el-table-column prop="status" label="Status" width="120" />
                <el-table-column prop="create_at" label="CreatedAt" width="180" sortable />
                <el-table-column prop="progress" label="ProgressID" />

                <el-table-column fixed="right" label="Actions" width="220">
                    <template #default="scope">
                        <el-button type="primary" plain size="small" @click="downloadFile(scope.row)"
                            style="margin-left: 1px">
                            <el-icon style="vertical-align: middle;margin-right: 5px;">
                                <Download />
                            </el-icon> Download
                        </el-button>
                        <el-button type="danger" plain size="small" @click="handleDelete(scope.row)"
                            style="margin-right: 10px">
                            <el-icon style="vertical-align: middle;margin-right: 5px;">
                                <Delete />
                            </el-icon> Delete
                        </el-button>
                    </template>
                </el-table-column>

                <template v-slot:empty>
                    <div>no report data</div>
                </template>

            </el-table>
        </div>

        <el-dialog v-model="createDialogFormVisible" width="50%" draggable @close="createDialogClose">
            <el-tabs v-model="activeName" @tab-click="handleClick" type="card">

                <el-tab-pane label="Upload XAS" name="first">
                    <el-form ref="createFormRef" :model="xasInfo" :rules="xasInfoRules" label-width="10px"
                        label-position="top">

                        <span style="margin-top: 20px;">Upload E-file</span>
                        <el-upload drag multiple :on-preview="handlePreview" :on-change="handleChange"
                            style="margin-top: 10px;" :on-remove="handleRemove" :before-remove="beforeRemove" :limit="1"
                            :file-list="fileList" :auto-upload="false">
                            <el-icon class="el-icon--upload">
                                <upload-filled />
                            </el-icon>
                            <div class="el-upload__text">
                                Drop e-file here or <em>click to upload</em>
                            </div>
                            <template #tip>
                                <div>
                                    The experimental spectra file to be read in. Must be .txt
                                </div>
                            </template>
                        </el-upload>

                        <el-form :inline="true" :model="xasInfo" :rules="xasInfoRules" style="margin-top: 30px;">
                            <el-form-item label="Column Energy" style="font-weight: bold;">
                                <el-input v-model="xasInfo.ce" clearable />
                            </el-form-item>

                            <el-form-item label="Column Number" style="font-weight: bold;">
                                <el-input v-model="xasInfo.cn" clearable />
                            </el-form-item>
                        </el-form>

                        <span style="margin-top: 20px;">Upload M-file</span>
                        <el-upload drag multiple :on-preview="handleFilesPreview" :on-change="handleFilesChange"
                            style="margin-top: 10px;" :on-remove="handleFilesRemove" :before-remove="beforeFilesRemove"
                            :limit="1" :file-list="fileTarList" :auto-upload="false">
                            <el-icon class="el-icon--upload">
                                <upload-filled />
                            </el-icon>
                            <div class="el-upload__text">
                                Drop m-file here or <em>click to upload</em>
                            </div>
                            <template #tip>
                                <div>
                                    Molecular geometry file to be read in e.g.Imidazole_geom.xyz
                                </div>
                            </template>
                        </el-upload>

                        <el-form :inline="true" :model="xasInfo" style="margin-top: 30px;">
                            <el-form-item label="Column Intensity" style="font-weight: bold;">
                                <el-input v-model="xasInfo.ci" clearable />
                            </el-form-item>

                            <el-form-item label="Offset" style="font-weight: bold;">
                                <el-input v-model="xasInfo.offset" clearable />
                            </el-form-item>
                        </el-form>

                    </el-form>
                </el-tab-pane>
            </el-tabs>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="cancelCreate">Cancel</el-button>
                    <el-button type="primary" @click="confirmCreate">Confirm</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
    import {
        Refresh,
        Delete,
        Upload,
        Download,
        UploadFilled
    } from '@element-plus/icons-vue'

    export default {
        data() {
            return {
                activeName: "first",

                fileList: [],
                fileTarList: [],

                xasInfo: {
                    ce: '',
                    cn: '',
                    ci: '',
                    offset: '',
                },
                xasInfoRules: {
                    ce: [{
                        required: true,
                        message: 'input ce',
                        trigger: 'blur'
                    }],
                    cn: [{
                        required: false,
                        message: 'input cn',
                        trigger: 'blur'
                    }],
                    ci: [{
                        required: false,
                        message: 'input ci',
                        trigger: 'blur'
                    }],
                    offset: [{
                        required: false,
                        message: 'input offset',
                        trigger: 'blur'
                    }],
                },

                loading: false,

                bookList: [],
                createDialogFormVisible: false,
                dialogFormVisible: false,
                autosize: {
                    minRows: 4,
                },
                createForm: {
                    name: '',
                    press: '',
                    label: '',
                    description: '',
                },
            }
        },
        created() {
            this.getReportList()
        },
        methods: {
            handleClick(tab, event) {
                if (this.activeName == "first") {
                    this.fileList = []
                } else {
                    this.createDialogClose()
                }
            },
            handleChange(file, fileList) {
                this.fileList = fileList
            },
            handleFilesChange(file, fileTarList) {
                this.fileTarList = fileTarList
            },
            handleRemove(file, fileList) {
                console.log(file, fileList)
            },
            handleFilesRemove(file, fileTarList) {
                console.log(file, fileTarList)
            },
            handlePreview(file) {
                console.log(file);
            },
            handleFilesPreview(file) {
                console.log(file);
            },
            beforeRemove(file, fileList) {
                return this.$confirm(`delete ${file.name}？`);
            },
            beforeFilesRemove(file, fileTarList) {
                return this.$confirm(`delete ${file.name}？`);
            },
            previewOnLine(report_id) {
                window.open('http://20.163.57.167:8888/report/html?report_id=' + report_id)
            },
            handleSelectionChange(val) {
                this.bulkValues = val
            },
            handleCascaderSelectChange(cascaderSelectValue) {
                if (cascaderSelectValue == null) {
                    this.pageInfo.cascader_label = ''
                    return
                }
                this.pageInfo.cascader_label = cascaderSelectValue.join("/")
            },
            handleClose(tag) {
                this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
            },
            showInput() {
                this.inputVisible = true;
                this.$nextTick(_ => {
                    this.$refs.saveTagInput.$refs.input.focus();
                });
            },
            handleInputConfirm() {
                let inputValue = this.inputValue;
                if (inputValue) {
                    this.dynamicTags.push(inputValue);
                }
                this.inputVisible = false;
                this.inputValue = '';
            },
            downloadFile(row) {
                let token = window.sessionStorage.getItem("token")
                window.open('http://20.163.57.167:8888/report/download?report_id=' + row.id)
            },
            createDialogClose() {
                this.$refs.createFormRef.resetFields()
                this.fileList = []
                this.fileTarList = []

                this.xasInfo.ce = ""
                this.xasInfo.cn = ""
                this.xasInfo.ci = ""
                this.xasInfo.offset = ""
            },
            async getReportList() {
                this.loading = true
                const user_name = window.sessionStorage.getItem('account')
                const {
                    data: res
                } = await this.$http.get('/report/list?user_name=' + user_name)
                this.loading = false
                if (res.code != 200) {
                    if (es.code != 401){
                        return this.$message.error('failed to get reports list');
                    }
                }
                this.bookList = res.result
            },
            handleCreate() {
                this.activeName = "first"
                this.createDialogFormVisible = true
            },
            confirmCreate() {
                if (this.fileList.length == 0) {
                    return this.$message.error('Please select uploading m-file')
                }
                if (this.fileTarList.length == 0) {
                    return this.$message.error('please select uploading m-file')
                }
                // TODO: 通过 Rules 实现
                if (this.xasInfo.ce == '') {
                    return this.$message.error('please input Column Energy')
                }
                if (this.xasInfo.cn == '') {
                    return this.$message.error('please input Column Number')
                }
                if (this.xasInfo.ci == '') {
                    return this.$message.error('please input Column Intensity')
                }
                if (this.xasInfo.offset == '') {
                    return this.$message.error('please input offset')
                }

                var file = this.fileList[0].raw
                var fileTar = this.fileTarList[0].raw

                // 只要点确定之后，之前选中的文件就清空
                this.fileList = []
                this.fileTarList = []
                this.createDialogFormVisible = false

                let fileFormData = new FormData()
                fileFormData.append('efile', file, file.name)
                fileFormData.append('mfiles', fileTar, fileTar.name)
                let requestConfig = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                }

                const userName = window.sessionStorage.getItem('account')
                this.$http.post("/report/upload?ce=" + this.xasInfo.ce + "&ci=" + this.xasInfo.ci + "&cn=" + this
                    .xasInfo.cn + "&offset=" + this.xasInfo.offset + "&user_name=" + userName, fileFormData,
                    requestConfig)
                    .then((res) => {
                        const data = res.data
                        if (data.code!=200){
                            return this.$message.error(data.message)
                        }

                        this.xasInfo.ce = ""
                        this.xasInfo.cn = ""
                        this.xasInfo.ci = ""
                        this.xasInfo.offset = ""

                        this.getReportList()
                        this.$message.success("upload xas success")
                    })
                    .catch((err) => {
                        this.$message.error(err.toString())
                    })
            },
            cancelCreate() {
                this.createDialogFormVisible = false
                this.xasInfo.ce = ""
                this.xasInfo.cn = ""
                this.xasInfo.ci = ""
                this.xasInfo.offset = ""
                this.createDialogClose()
            },
            async handleDelete(row) {
                this.$confirm('Proxy will permanently delete the file. Continue?', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                    draggable: true,
                })
                    .then(() => {
                        const userName = window.sessionStorage.getItem('account')
                        this.$http.delete("/report/delete?report_id=" + row.id+"&user_name=" + userName)
                            .then((res) => {
                                const data = res.data
                                if (data.code != 200) {
                                    return this.$message.error(data.message)
                                }
                                this.getReportList()
                                return this.$message.success(row.name + " delete success")
                            })
                            .catch((err) => {
                                return this.$message.error(err.toString())
                            })
                    })
                    .catch(() => { })
            }
        },
        components: {
            Delete,
            Upload,
            Download,
            Refresh,
            UploadFilled
        }
    }
</script>

<style scoped>
    .el-icon {
        vertical-align: middle;
        text-align: center;
    }
</style>