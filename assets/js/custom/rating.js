
                    // console.log("hello world!")

                    const one = document.getElementById('first')
                    const two = document.getElementById('second')
                    const three = document.getElementById('third')
                    const four = document.getElementById('fourth')
                    const five = document.getElementById('fifth')


                    // console.log(one)

                    const form = document.querySelector('.rate-form')

                    

                    const handleStarSelect = (size) => {
                        const children = form.children
                        // console.log(children[0])
                        for (let i=0; i < children.length; i++) {
                            if(i < size) {
                                children[i].classList.add('checked')
                            } else {
                                children[i].classList.remove('checked')
                            }
                        }
                    }

                    const handleSelect = (selection) => {
                        switch(selection){
                            case 'first': {
                                handleStarSelect(1);
                                return
                            }
                            case 'second': {
                                handleStarSelect(2);
                                return
                            }
                            case 'third' : {
                                handleStarSelect(3);
                                return
                            }
                            case 'fourth' : {
                                handleStarSelect(4);
                                return
                            }
                            case 'fifth' : {
                                handleStarSelect(5);
                                
                            }
                        }
                    }

                    // to conver the string value of rating into numerics
                    const getNumericValue = (stringValue) =>{
                        let numericValue;
                        if (stringValue === 'first') {
                            numericValue = 1
                        } 
                        else if (stringValue === 'second') {
                            numericValue = 2
                        }
                        else if (stringValue === 'third') {
                            numericValue = 3
                        }
                        else if (stringValue === 'fourth') {
                            numericValue = 4
                        }
                        else if (stringValue === 'fifth') {
                            numericValue = 5
                        }
                        else {
                            numericValue = 0
                        }
                        return numericValue
                    }
                    





                    const arr = [one, two, three, four, five]

                    arr.forEach(item=> item.addEventListener('mouseover', (event)=>{
                        handleSelect(event.target.id)
                    }))

                    arr.forEach(item=> item.addEventListener('click', (event)=>{
                        const rate = getNumericValue(event.target.id);
                        document.getElementById('rate').value = rate;
                        // console.log(rate)
                    }))