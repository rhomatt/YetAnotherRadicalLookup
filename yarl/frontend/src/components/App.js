import React from 'react';
import HomePage from './HomePage';
import About from './About';
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from 'react-router-dom';

export default function App(){
    return (
        <Router>
            <Switch>
                <Route path='/About'>
                    <About/>
                </Route>
                <Route path='/'>
                    <HomePage/>
                </Route>
                <Route path='/Acknowledgements'>
                    <Acknowledgements/>
                </Route>
            </Switch>
        </Router>
    );
}
