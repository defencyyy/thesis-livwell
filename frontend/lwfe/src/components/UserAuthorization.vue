<template>
    <div>
        <div v-bind:key="todo.id" v-for="todo in authorize">
            <p>{{todo.title}}</p>

        </div>
    </div>
</template>
<script>
export default {
    name: "UserAuthorization",
    components:{

    },
    props: ["authorize"]
    // data(){
    //     return{
    //         msg:"Hello, Worlds!"
    //     }
    // }
}
</script>
<style scoped>

</style>