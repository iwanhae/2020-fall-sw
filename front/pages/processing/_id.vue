<template>
  <div class="container">
    <div>
      <Logo />
      <h1 class="title">
        keyword
      </h1>
      <h2>{{ message }}</h2>
      <h2>{{ current }} / {{ total }}</h2>
      <el-progress type="circle" :percentage="Math.floor(current / total * 100)" />
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      id: this.$route.params.id,
      message: 'tmp',
      current: 0,
      total: 1
    }
  },
  mounted () {
    this.loading()
  },
  methods: {
    async loading (e) {
      try {
        const res = await this.$axios.get(`/progress/${this.id}`)
        this.message = res.data.message
        this.current = res.data.current
        this.total = res.data.total
        if (this.current !== this.total) {
          setTimeout(this.loading, 500)
        } else {
          this.$router.push(`/${this.id}`)
        }
      } catch (err) {
        this.$message({
          showClose: true,
          message: err,
          type: 'error'
        })
        setTimeout(this.loading, 500)
      }
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
