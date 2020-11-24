<template>
  <div style="width:100%;">
    <div style="width: 1024px;margin: 0px auto;text-align: center;">
      <h1 class="title" style="margin:0 auto;">
        keyword
      </h1>
      <br>
      <div style="display:flex">
        <div style="width: 512px;display: block;">
          입력
          <canvas id="request" width="400" height="400" style="position: fixed;" />
        </div>
        <div style="width: 512px;display: block;">
          결과
          <div v-for="r in related" :key="r.keyword">
            <h3 class="title" style="font-size: xxx-large;">
              {{ r.keyword }} - {{ 100 - (Math.floor(r.similarity * 10000) / 100) }}%
            </h3>
            <canvas :id="r.keyword" width="400" height="400" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js'

export default {
  data () {
    return {
      id: this.$route.params.id,
      related: []
    }
  },
  async mounted () {
    const res = await this.$axios.get(`/result/${this.id}`)
    console.log(res.data)
    this.related = res.data.related
    const data = res.data.data.map((e) => {
      return {
        x: new Date(e.date * 1000),
        y: e.value
      }
    })

    setTimeout(() => {
      this.showGraph('request', 'Your data', data)
      this.related.forEach((e) => {
        const data = e.data.map((e) => {
          return {
            x: new Date(e.date * 1000),
            y: e.value
          }
        })
        this.showGraph(e.keyword, e.keyword, data)
      })
    }, 500)
  },
  methods: {
    dynamicColors () {
      const r = Math.floor(Math.random() * 255)
      const g = Math.floor(Math.random() * 255)
      const b = Math.floor(Math.random() * 255)
      return 'rgb(' + r + ',' + g + ',' + b + ')'
    },
    showGraph (id, title, data) {
      const ctx = document.getElementById(id)
      // eslint-disable-next-line no-new
      new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [{
            label: title,
            data,
            borderColor: this.dynamicColors(),
            fill: false
          }]
        },
        options: {
          tooltips: {
            mode: 'index',
            intersect: false
          },
          hover: {
            mode: 'nearest',
            intersect: true
          },
          scales: {
            xAxes: [{
              type: 'time'

            }]
          }
        }
      })
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
