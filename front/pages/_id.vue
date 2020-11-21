<template>
  <div class="container">
    <div>
      <Logo />
      <h1 class="title">
        keyword
      </h1>
      <br>
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
