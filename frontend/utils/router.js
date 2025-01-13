import ServicsCard from "../components/ServicsCard.js";
import LoginPage from "../pages/LoginPage.js";
import RegisterPage from "../pages/RegisterPage.js";
import SrevicesList from "../pages/SrevicesList.js";
import ServiceDisplay from "../pages/ServiceDisplay.js";
import store from "./store.js";
import AdminDashboard from "../pages/admin/AdminDashboard.js";
import CompleteProfileCustomer from "../pages/customer/CompleteProfileCustomer.js";
import CompleteProfileProf from "../pages/prof/CompleteProfileProf.js";
import ProfManagement from "../pages/admin/ProfManagement.js";
import CustomerRequest from "../pages/customer/CustomerRequest.js";
import ProfDashbord from "../pages/prof/ProfDashbord.js";
import ReqProfessional from "../pages/prof/ReqProfessional.js";
import NewService from "../pages/admin/NewService.js";
import Block from "../pages/admin/Block.js";

const Home = {
  template: `<h1> This is Home </h1>`,
};

const routes = [
  { path: "/", component: SrevicesList },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  {
    path: "/service/:id",
    component: ServiceDisplay,
    props: true,
    meta: { requiresLogin: true },
  },
  {
    path: "/admin-dashboard",
    component: AdminDashboard,
    meta: { requiresLogin: true, role: "Admin" },
  },
  { path: "/customerCompleteProfile", component: CompleteProfileCustomer },
  { path: "/professionalCompleteProfile", component: CompleteProfileProf },
  { path: "/profManagement", component: ProfManagement,  meta: { requiresLogin: true, role: "Admin" }},
  { path: "/request", component: CustomerRequest },
  { path: "/profDashboard", component: ProfDashbord },
  { path: "/reqManagement", component: ReqProfessional,  meta: { requiresLogin: true, role: "Professional" }},
  { path: "/newService", component: NewService,  meta: { requiresLogin: true, role: "Admin" }},
  { path: "/blockUser", component: Block,  meta: { requiresLogin: true, role: "Admin" }},

];
const router = new VueRouter({
  routes,
});

// navigation guards
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresLogin)) {
    if (!store.state.loggedIn) {
      console.log("Here");
      next({ path: "/login" });
    } else if (to.meta.role && to.meta.role != store.state.role) {
      alert("role not authorized");
      next({ path: "/" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
