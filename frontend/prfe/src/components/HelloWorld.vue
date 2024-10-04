<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Click here to check the full requirements in condominium <br>
      <a href="https://www.ombudsman.gov.ph/docs/republicacts/Republic_Act_No_3019.pdf" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>

    <h1>GET YOUR OWN UNIT NOW AT TREES RESIDENCES SMDC </h1>
    <h2>FOR AS LOW AS ₱10,000+ MONTHLY! 5% SPOT DOWNPAYMENT TO MOVE IN! </h2>
    <h4>NEAR SM FAIRVIEW </h4> 
    <h4>PROMO: Reserve NOW and get up to 300,000 Discounts READY TO MOVE-IN UNITS</h4>

    <h6> • STUDIO UNIT | ₱84,000+ SPOT DP | ₱10,000+MONTHLY <br>
        • 1 BEDROOM UNIT | ₱110,000+ SPOT DP | ₱13,000+ MONTHLY <br>
        • 2 BEDROOM UNIT | ₱170,000+SPOT DP | ₱20,000+
    </h6>
   
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
