import ServicsCard from "../components/ServicsCard.js";
import LoginPage from "../pages/LoginPage.js";
import RegisterPage from "../pages/RegisterPage.js";
import SrevicesList from "../pages/SrevicesList.js";
import ServiceDisplay from "../pages/ServiceDisplay.js";
import store from "./store.js";
import AdminDashboard from "../pages/AdminDashboard.js";
import CompleteProfileCustomer from "../pages/CompleteProfileCustomer.js";
import CompleteProfileProf from "../pages/CompleteProfileProf.js";


const Home = {
  template: `<h1> This is Home </h1>`,
};


const routes = [
  { path: "/", component: Home },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  { path: "/services", component: SrevicesList },
  { path: "/service/:id", component: ServiceDisplay, props: true, meta: {requiresLogin : true} },
  { path: "/admin-dashboard", component: AdminDashboard,  meta: {requiresLogin : true, role: "Admin"} },
  {path: "/customerCompleteProfile", component: CompleteProfileCustomer},
  {path: "/professionalCompleteProfile", component: CompleteProfileProf}
  
];
const router = new VueRouter({
  routes
})

// navigation guards
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresLogin)){
      if (!store.state.loggedIn){
        console.log("Here")
          next({path : '/login'})
      } else if (to.meta.role && to.meta.role != store.state.role){
          alert('role not authorized')
           next({path : '/'})
      } else {
          next();
      }
  } else {
      next();
  }
})


export default router;
