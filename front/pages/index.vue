<template>
  <div class="container">
    <div>
      <Logo />
      <h1 class="title">
        keyword
      </h1>
      <h5>2020년 2학기 서울시립대학교 소프트웨어응용</h5>
      <h2>1조: 김현구, 이완해, 정진용</h2>
      <br>
      <el-upload
        class="upload-demo"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        :before-upload="beforeUpload"
        :auto-upload="true"
        :limit="1"
        :http-request="upload"
        :multiple="false"
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <div slot="tip" class="el-upload__tip">
          only csv file can be uploaded
        </div>
      </el-upload>
      <div class="links">
        <a
          href="https://github.com/iwanhae/2020-fall-sw"
          target="_blank"
          rel="noopener noreferrer"
          class="button--grey"
        >
          GitHub
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      fileList: []
    }
  },
  methods: {
    beforeUpload (file) {
      console.log(file)
      if (file.name.endsWith('.csv')) {
        return true
      }
      this.$message({
        showClose: true,
        message: 'CSV 파일만 업로드가 가능합니다!',
        type: 'warning'
      })
      return false
    },
    async upload (e) {
      console.log(e)
      console.log(e.file.size)
      if (e.file.size > 1024 * 1024 * 2) {
        return false
      }
      const fulltext = await e.file.text()
      const data = []
      fulltext.split('\n').forEach((line) => {
        const tmp = line.split(',')
        const date = new Date(tmp[0])
        const value = parseFloat(tmp[1])
        if (!isNaN(value)) {
          data.push({
            date, value
          })
        }
      })
      console.log(data)
      if (data.length !== 0) {
        try {
          const res = await this.$axios.post('/request', data)
          console.log(res)
          const id = res.data.id
          this.$router.push(`/processing/${id}`)
        } catch (e) {
          this.$message({
            showClose: true,
            message: e,
            type: 'error'
          })
          return false
        }

        return true
      }
      this.$message({
        showClose: true,
        message: '데이터를 못찾았어요 :-(',
        type: 'warning'
      })
      return false
    }
  }
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
