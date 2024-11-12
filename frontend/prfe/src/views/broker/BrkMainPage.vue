<template>
  <Header>
    <HeaderLivwell/>
  </Header>
  <div class="main-page">
    <SideNav />
    <div class="content">
      <div>
        <h1>Gwynn Rafer Cujardo</h1>
        <h5>@gwynncujardo</h5>
      <!-- <p>This is the main page for brokers.</p>
      <button @click="logout">Logout</button> -->
      </div>

      <div class="contentpage py-5 mx-2" style="width: 100%; height: 80%;">
        <div>
          <div class="content1" style="height: 30%;"><h2>Total Sales:</h2></div>
          <div class="content2" style="height: 30%;"><h2>Milestones Achieved:</h2></div>
          <div class="content4">
            <h2>Broker of the Month</h2>
            <div>
             
            <img src="https://th.bing.com/th/id/OIP.2nSUJDGTSglEgp0sQw_R8AHaKu?rs=1&pid=ImgDetMain" alt="" width="250px" height="200px">
           
          </div>
          </div>
        </div>
        <div>
          <div class="content3"><h2>Analytics</h2></div>
           
        </div>

      </div>
    </div>
  </div>


</template>

<script>
import SideNav from "@/components/SideNav.vue";
import HeaderLivwell from "@/components/HeaderLivwell.vue";

export default {
  name: "BrkMainPage",
  components: {
    SideNav, HeaderLivwell,
  },
  methods: {
    logout() {
      localStorage.removeItem("authToken");
      localStorage.removeItem("logged_in");
      localStorage.removeItem("user_role");

      this.$router.push({ path: "/home" });
    },
  },
};
</script>

<style scoped>

header
{
  background-color: #42b983;
}

.main-page {
  display: flex;
  height: 100vh;
 
}

.content {
  flex: 1;
  padding: 20px;
  text-align: center;
}
.contentpage
{
  border: 1px solid black;
  
}
.content h1, h5 {
  color: black;
  text-align: left;
  padding-left: 50px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
}

.content1, .content2
{
  
  text-align: left;
  background-color: #D9D9D9 ;
  height: 30%;
  border-radius: 10px;
  padding-left: 10px;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 50px;

}
.content1 h2, .content2 h2
{
  padding-right: 30px;
}
.content3{
  text-align: center;
  background-color: #D9D9D9;
  border-radius: 10px;
  padding-left: 10px;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 20px;
  height: 60%;
  width: 500%;
  

  
}
.content3 h2
{
  text-align: center;
  padding-top: 20px;
}

.content4
{
  background-color: #D9D9D9;
  border-radius: 10px;
  height: 40%;
  width: 200%;
  margin-bottom: 20px;
  margin-right: 20px;
  margin-left: 50px;
  padding-left: 20px;
  text-align: start;
}
.content img
{
  margin-left: 10px;
}
.contentpage
{
  display: flex;
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
</style>
