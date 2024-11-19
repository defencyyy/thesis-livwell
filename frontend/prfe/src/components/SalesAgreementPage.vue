<template>
  <div v-if="agreement">
    <h2>Sales Agreement for {{ agreement.customer_name }}</h2>
    <p><strong>Unit Title:</strong> {{ agreement.unit_title }}</p>
    <p><strong>Unit Price:</strong> {{ agreement.unit_price }}</p>
    <p><strong>Payment Plan:</strong> {{ agreement.payment_plan }}</p>
    <p><strong>Spot Discount:</strong> {{ agreement.spot_discount }}</p>
    <p><strong>Net Unit Price:</strong> {{ agreement.net_unit_price }}</p>
    <p><strong>Total Amount Payable:</strong> {{ agreement.total_amount_payable }}</p>
    <p><strong>Reservation Fee:</strong> {{ agreement.reservation_fee }}</p>
    <p><strong>Net Full Payment:</strong> {{ agreement.net_full_payment }}</p>
    <p><strong>Spot Downpayment:</strong> {{ agreement.spot_downpayment }}</p>
    <p><strong>Spread Downpayment:</strong> {{ agreement.spread_downpayment }}</p>
    <p><strong>Payable Months:</strong> {{ agreement.payable_months }}</p>
    <p><strong>Payable Per Month:</strong> {{ agreement.payable_per_month }}</p>
    <p><strong>Balance Upon Turnover:</strong> {{ agreement.balance_upon_turnover }}</p>
    <p><strong>Created At:</strong> {{ agreement.created_at }}</p>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      agreement: null,
    };
  },
  methods: {
    async fetchSalesAgreement() {
      const uuid = this.$route.params.uuid;  // Get the UUID from the route parameters
      try {
        const response = await axios.get(`/sales-agreement/${uuid}/`);
        this.agreement = response.data;
      } catch (error) {
        console.error('Error fetching sales agreement:', error);
        // Handle error (e.g., show an error message)
      }
    },
  },
  mounted() {
    this.fetchSalesAgreement();
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
