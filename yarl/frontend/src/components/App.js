import React from 'react';
import HomePage from './HomePage';
import About from './About';
import Acknowledgements from './Acknowledgements';
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
                <Route path='/Acknowledgements'>
                    <Acknowledgements/>
                </Route>
                <Route path='/'>
                    <HomePage/>
                </Route>
            </Switch>
        </Router>
    );
}
