var ops = [];
db.test.find({ "accepted": { "$type": 2} }).forEach(doc => {
     var children = doc.children.split(',').map( e => e.replace("[",'').toString() );
     print(children)
     ops.push({
       "updateOne": {
         "filter": { "_id": doc._id },
         "update": { "$set": { "accepted": children } }
       }
     });

     if ( ops.length >= 1000 ) {
       db.test2.bulkWrite(ops);
       ops = [];
     }
});

if ( ops.length > 0 ) {
     db.test2.bulkWrite(ops);
     ops = [];
}
db.test.find()


 db.rakutan2020.find().forEach(function (el) {
    el.accepted=el.accepted.substring(1,el.accepted.length-1);
    el.accepted = el.accepted.split(',').map(Number);
         db.rakutan2020.save(el);
});
 db.rakutan2020.find().forEach(function (el) {
    el.total=el.total.substring(1,el.total.length-1);
    el.total = el.total.split(',').map(Number);
         db.rakutan2020.save(el);
});