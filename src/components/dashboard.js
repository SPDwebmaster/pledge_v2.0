import React from 'react';
import autobind from 'class-autobind';
import { readRemoteFile } from 'react-papaparse';
import Marks from './marks'
import './dashboard.css'

const COL_DATE = 0
const COL_PLEDGE_NAME = 1
const COL_SUBMISSION_TYPE = 2
const COL_BROTHER_NAME = 3
const COL_MARK_TYPE = 5
const COL_MARK_COUNT = 6
const COL_DESCRIPTION = 7
const COL_APPROVED = 9

const KEY_IS_MARK = "White/Black Mark (For Brothers)"

export default class DashBoard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {pc: null};
        autobind(this);
        this.getData();
    }
    async getData() {
        readRemoteFile("https://docs.google.com/spreadsheets/d/e/2PACX-1vTpZTBbl4UauVo_30ZTW-rp4xYPm_NiKDAyWAp-yOyFYUY8Se7RZqaWfJIBuBI2vFNpcJnUbfTRPp0u/pub?output=csv", {
            complete: (results) => {
                console.log(results)
                let submissionData = results.data.slice(1)
                let pledge_class_name = results.data[1]?.[16]
                
                this.props.setPledgeClassName("T Class")

                const marks = submissionData.filter(row => row[COL_SUBMISSION_TYPE] === KEY_IS_MARK && row[COL_APPROVED] === "yes").map(row => new Mark(new Date(row[COL_DATE]).toDateString(), row[COL_BROTHER_NAME], row[COL_PLEDGE_NAME], row[COL_MARK_TYPE], parseInt(row[COL_MARK_COUNT]), row[COL_DESCRIPTION], row[COL_APPROVED]))
                const pledgeDict = {}

                // collect class-marks separately
                const classMarks  = []


                marks.forEach((mark) => {
                    if (mark.pledge === "All") {
                        classMarks.push(mark)
                        return
                    }
                    const pledges = mark.pledge.split(", ")

                    // Marks can be assigned to more than one pledge
                    pledges.forEach(pledge => {
                        if (!pledgeDict[pledge]) {
                            pledgeDict[pledge] = new Pledge(pledge)
                        }
                        pledgeDict[pledge].marks.push(mark)
                    })
                })

                const pledges = Object.values(pledgeDict)
                pledges.forEach(pledge => pledge.marks = [...pledge.marks, ...classMarks])

                this.setState({pc: Object.values(pledgeDict)})
            },
          });
    }

    openPledge(pledge) {
        this.setState({open: pledge.name === this.state.open ? undefined: pledge.name});
    }

    render() {
        let pc = this.state.pc;
        let open = this.state.open;

        if (!pc)
            return (
            <div className="dash">
                <div className="loader"/>
            </div>);

        let MarkDetails = (marks) => {
            let details = []
            marks.forEach(m => {
                details.push(
                <tr key={m.desc} className="details">
                    <td><Marks type={m.type} count={m.count}/></td>
                    <td>{m.date}</td>
                    <td>{m.brother + ' - ' + m.desc}</td>
                </tr>)
            });
            return details;
        }

        

        const PledgeRow = (pledge) => {
            return(
                <tr key={pledge.name} onClick={() => this.openPledge(pledge)} className={this.state.open === pledge.name ? "details" : ""}>
                    <td>{pledge.name}</td>
                    <td><Marks type="black" count={pledge.getTotal("Black")}/></td>
                    <td><Marks type="white" count={pledge.getTotal("White")}/></td>
                </tr>)
        }

        let rows = [];
        pc.forEach(p => {
            rows.push(PledgeRow(p));
            if (open === p.name) {
                rows.push(MarkDetails(p.marks))
            }
        })
            
        return(
            <div className="dash">
                <table>
                    <tbody>
                        <tr>
                            <th width="25%">
                                pledge
                            </th>
                            <th width="20%">
                                black
                            </th>
                            <th >
                                white
                            </th>
                        </tr>
                        {rows}
                    </tbody>
                </table>
                <br></br>
            </div>
        )
    }
}

class Mark {
    constructor(date, brother, pledge, type, count, desc, approved) {
    this.date = date
    this.brother = brother
    this.pledge = pledge
    this.type = type
    this.count = count
    this.desc = desc
    this.approved = approved
    }
}

class Pledge {
    constructor(name) {
        this.name = name;
        this.marks = [];
    }

    getTotal(type) {
        let total = 0;
        for (let i in this.marks) {
            if (this.marks[i].type === type)
                total += this.marks[i].count;
        }

        return total;
    }
}
