export default {
    template: `
    <div>
        <input placeholder="email" v-model="email"/>
        <input placeholder="password" v-model="password"/>
        <button @click="submitLogin">Log in</button>
    </div>
    `,
    data(){
        return{
        email: null,
        password: null,}
    },
    methods : {
        async submitLogin(){
            const res = await fetch(location.origin+'/login',{
                method: 'POST',
                headers:{'Content-Type': 'application/json'},
                body: JSON.stringify({'email': this.email,'password': this.password})
            })
            if(res.ok){
                console.log("We are Logged In")
                const data = await res.json()
                console.log(data)
                localStorage.setItem('user', JSON.stringify(data))
                 
                this.$store.commit('setUser')
                this.$router.push('/services')
            }
        }
    }
}