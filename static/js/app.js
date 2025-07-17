/**
 * DiskClean 前端应用逻辑
 * @description 负责与后端API交互、数据处理和页面渲染
 */
new Vue({
    el: '#app',
    data: {
        drives: [],          // 存储可用磁盘分区列表
        selectedDrive: '',   // 当前选择的磁盘分区
        directories: [],     // 存储目录大小信息
        loading: false,      // 加载状态标志
        error: null          // 错误信息
    },
    mounted() {
        // 页面加载完成后获取磁盘分区列表
        this.getDrives();
    },
    methods: {
        /**
         * 获取系统磁盘分区列表
         * @description 从后端API获取并更新drives数据
         */
        async getDrives() {
            try {
                this.loading = true;
                this.error = null;
                const response = await fetch('/api/drives');
                if (!response.ok) throw new Error('获取磁盘分区失败');
                this.drives = await response.json();
                // 默认选择第一个磁盘分区
                if (this.drives.length > 0) {
                    this.selectedDrive = this.drives[0].path;
                    this.getDirectorySizes();
                }
            } catch (err) {
                this.error = err.message;
                console.error('获取磁盘分区错误:', err);
            } finally {
                this.loading = false;
            }
        },

        /**
         * 获取选定分区的目录大小信息
         * @description 从后端API获取并按大小排序目录数据
         */
        async getDirectorySizes() {
            if (!this.selectedDrive) return;

            try {
                this.loading = true;
                this.error = null;
                const response = await fetch(`/api/directories?path=${encodeURIComponent(this.selectedDrive)}`);
                if (!response.ok) throw new Error('获取目录大小失败');
                const data = await response.json();
                // 按大小降序排序目录
                this.directories = data.sort((a, b) => b.size - a.size);
            } catch (err) {
                this.error = err.message;
                console.error('获取目录大小错误:', err);
            } finally {
                this.loading = false;
            }
        },

        /**
         * 删除指定目录
         * @param {string} path - 要删除的目录路径
         */
        async deleteDirectory(path) {
            if (!confirm(`确定要删除目录: ${path} 吗? 此操作不可恢复!`)) {
                return;
            }

            try {
                this.loading = true;
                this.error = null;
                const response = await fetch(`/api/delete?path=${encodeURIComponent(path)}`, {
                    method: 'DELETE'
                });
                if (!response.ok) throw new Error('删除目录失败');
                // 删除成功后刷新目录列表
                this.getDirectorySizes();
                alert('目录删除成功');
            } catch (err) {
                this.error = err.message;
                console.error('删除目录错误:', err);
            } finally {
                this.loading = false;
            }
        },

        /**
         * 格式化文件大小显示
         * @param {number} bytes - 字节数
         * @returns {string} 格式化后的大小字符串
         */
        formatSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }
    }
});
