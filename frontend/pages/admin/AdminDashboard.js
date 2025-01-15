export default {
    template: `
        <div class="container mt-5">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white">
                    <h1 class="text-center">Welcome Admin</h1>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        <router-link 
                            to="/profManagement" 
                            class="list-group-item list-group-item-action">
                            New Professional Acceptance
                        </router-link>
                        <router-link 
                            to="/newService" 
                            class="list-group-item list-group-item-action">
                            Add New Service
                        </router-link>
                        <router-link 
                            to="/blockUser" 
                            class="list-group-item list-group-item-action">
                            Block/Unblock an Existing User
                        </router-link>
                        <router-link 
                            to="/editService" 
                            class="list-group-item list-group-item-action">
                            Edit a Service
                        </router-link>
                        
                    </div>
                </div>
                <div class="card-footer text-center">
                    <small class="text-muted">Made by Aryan Kohli | 22f3001832</small>
                </div>
            </div>
        </div>
    `
}
