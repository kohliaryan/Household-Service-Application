import Navbar from "./components/Navbar.js";
import router from "./utils/route.js";
const app = new Vue({
  el: "#app",
  template: `
    <div>
        <Navbar/>
        <router-view/>
    </div>
    `,
  components: {
    Navbar,
  },
  router,
});
