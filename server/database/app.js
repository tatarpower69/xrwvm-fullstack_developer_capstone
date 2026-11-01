const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const app = express();
const Reviews = require('./review');
const Dealerships = require('./dealership');
app.use(express.json({limit: '64kb'}));
const route = (handler) => async (req,res,next) => { try { await handler(req,res); } catch(error) { next(error); } };
app.get('/', (req,res) => res.send('Welcome to the Mongoose API'));
app.get('/fetchReviews', route(async(req,res) => res.json(await Reviews.find().lean())));
app.get('/fetchReviews/dealer/:id', route(async(req,res) => res.json(await Reviews.find({dealership: Number(req.params.id)}).lean())));
app.get('/fetchDealers', route(async(req,res) => res.json(await Dealerships.find().lean())));
app.get('/fetchDealers/:state', route(async(req,res) => res.json(await Dealerships.find({state: req.params.state}).lean())));
app.get('/fetchDealer/:id', route(async(req,res) => res.json(await Dealerships.find({id: Number(req.params.id)}).lean())));
const counterSchema = new mongoose.Schema({_id: String, value: Number});
const Counter = mongoose.model('counter', counterSchema);
app.post('/insert_review', route(async(req,res) => {
  const data = req.body;
  if (!Number.isInteger(data.dealership) || !data.review?.trim() || !data.name?.trim()) return res.status(400).json({error:'Invalid review'});
  if (!(await Dealerships.exists({id:data.dealership}))) return res.status(404).json({error:'Dealer not found'});
  const counter = await Counter.findByIdAndUpdate('reviews', {$inc:{value:1}}, {new:true});
  const review = await Reviews.create({...data, id:counter.value});
  res.status(201).json(review);
}));
app.use((error,req,res,next) => { console.error(error.message); res.status(error.name==='ValidationError'?400:500).json({error:'Request failed'}); });
async function start() {
  await mongoose.connect(process.env.MONGO_URL || 'mongodb://localhost:27017/dealershipsDB');
  for (const [Model,file,key] of [[Reviews,'reviews.json','reviews'],[Dealerships,'dealerships.json','dealerships']]) {
    if (await Model.countDocuments() === 0) await Model.insertMany(JSON.parse(fs.readFileSync(path.join(__dirname,'data',file),'utf8'))[key]);
  }
  const latest = await Reviews.findOne().sort({id:-1}).lean();
  await Counter.updateOne({_id:'reviews'}, {$max:{value:latest?.id || 0}}, {upsert:true});
  app.listen(process.env.PORT || 3030, '0.0.0.0', () => console.log('Dealership API ready on port ' + (process.env.PORT || 3030)));
}
start().catch(error => {console.error(error);process.exit(1)});
