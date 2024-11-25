<template>
  <div class="main-page">
    <SideNav />
    <div class="content">
      <h1>Hi, {{ brokerName }}</h1>
      <p>{{ brokerEmail }}</p>
      <strong>Total Sales:</strong> {{ totalSales }}
      <strong>Total Commissions:</strong> {{ totalCommissions }}
      <p>Total Customers: {{ totalCustomers }}</p>

      <!-- Display Total Sales Status -->
      <div>
        <p><strong>Sold:</strong> {{ salesStatus.sold }}</p>
        <p><strong>Pending Reservation:</strong> {{ salesStatus.pending }}</p>
        <p><strong>Reserved:</strong> {{ salesStatus.reserved }}</p>
      </div>

      <!-- Pie chart displaying sales status -->
      <div class="pie-chart-container">
        <PieChart :sold="salesStatus.sold" :pending="salesStatus.pending" :reserved="salesStatus.reserved" />
      </div>

      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";
import PieChart from "@/components/PieChart.vue";  // Import the PieChart component

export default {
  name: "BrkMainPage",
  components: {
    SideNav,
    PieChart,  // Register the PieChart component
  },
  data() {
    return {
      brokerName: '',
      brokerEmail: '',
      totalSales: 0,
      totalCommissions: 0,
      totalCustomers: 0,
      salesStatus: {
        sold: 0,
        pending: 0,
        reserved: 0,
      },
    };
  },
  created() {
    this.fetchBrokerInfo();
  },
  methods: {
    async fetchBrokerInfo() {
      const brokerId = localStorage.getItem('broker_id');
      try {
        const response = await fetch(`http://localhost:8000/brokers/${brokerId}/`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` },
        });
        const data = await response.json();
        if (data.success !== false) {
          this.brokerName = `${data.f_name} ${data.l_name}`;
          this.brokerEmail = data.email;
        } else {
          console.error('Broker info not found or error:', data.message);
        }
      } catch (error) {
        console.error('Error fetching broker info:', error);
      }

      const salesResponse = await fetch(`http://localhost:8000/sales/total/?broker_id=${brokerId}`);
      if (salesResponse.ok) {
        const salesData = await salesResponse.json();
        this.totalSales = salesData.total_sales;
      }

      const commissionsResponse = await fetch(`http://localhost:8000/sales/commissions/?broker_id=${brokerId}`);
      if (commissionsResponse.ok) {
        const commissionsData = await commissionsResponse.json();
        this.totalCommissions = commissionsData.total_commissions;
      }

      const customersResponse = await fetch(`http://localhost:8000/customers/broker/${brokerId}/?include_sales=false`);
      if (customersResponse.ok) {
        const customersData = await customersResponse.json();
        this.totalCustomers = customersData.total_customers;
      }

      const salesStatusResponse = await fetch(`http://localhost:8000/sales/?broker_id=${brokerId}`);
      if (salesStatusResponse.ok) {
        const statusData = await salesStatusResponse.json();
        if (statusData.success) {
          this.salesStatus = statusData.sales_status_data;
        }
      }
    },

    logout() {
      localStorage.removeItem("authToken");
      localStorage.removeItem("logged_in");
      localStorage.removeItem("user_role");
      localStorage.removeItem("user_id");
      localStorage.removeItem("company_id");

      this.$router.push({ path: "/home" });
    },
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}

h1 {
  color: #42b983;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #ff1a1a;
}

.pie-chart-container {
  width: 50%;
  margin: 20px auto;
}
</style>
