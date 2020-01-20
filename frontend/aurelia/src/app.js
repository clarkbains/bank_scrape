
import './gateway';
import { Gateway } from './gateway';
export class App {
  configureRouter(config, router) {
    config.title = 'Bank Scrape';
    config.map([
      {
        route: ['', 'welcome'],
        name: 'welcome',
        moduleId: './views/welcome',
        nav: true,
        title: 'Home',
        settings: {root:this}
      },
      {
        route: 'login',
        name: 'login',
        moduleId: './views/login',
        nav: true,
        title: 'Login',
        settings: {root:this}
      },
      {
        route: 'admin',
        name: 'admin',
        moduleId: './views/admin',
        nav: true,
        title: 'admin'
      }
    ]);
    this.features = null
    this.router = router;
    this.gateway = new Gateway({host:"http://localhost:8000"})
  }
}
