import React from 'react';
import autobind from 'class-autobind';
import m1 from '../m1.png';
import m2 from '../m2.png';
import m3 from '../m3.png';
import m4 from '../m4.png';
import m5 from '../m5.png';
import './dashboard.css'

const mark_images = [m1,m2,m3,m4,m5];

export default class Marks extends React.Component {
    constructor(props) {
        super(props);
        autobind(this);
    }

    render() {

        if (!this.props.count)
            return <div/>

        let display = [];

        let Mark = (i, img) => {
            return(
                <img className={`${this.props.type.toLowerCase()} mark`} key={`mark${i}`} src={img} alt="mark"/>
            )
        }

        let i;
        for (i = 5; i <= this.props.count; i+=5) {
            display.push(Mark(i,m5));
        }

        let rem = this.props.count % 5;

        if (rem !== 0)
            display.push(Mark(i,mark_images[rem - 1]));

        return(
            <div>
                {display}
            </div>
        )
    }
}