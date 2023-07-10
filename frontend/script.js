// Populate datalist with a large list of symptoms
document.addEventListener("DOMContentLoaded", function() {
    var symptoms = ['Itching', 'Skin rash', 'Nodal skin eruptions', 'Dischromic patches', 'Continuous sneezing', 'Shivering', 'Chills', 'Watering from eyes', 'Stomach pain', 'Acidity', 'Ulcers on tongue', 'Vomiting', 'Cough', 'Chest pain', 'Yellowish skin', 'Nausea', 'Loss of appetite', 'Abdominal pain', 'Yellowing of eyes', 'Burning micturition', 'Spotting urination', 'Passage of gases', 'Internal itching', 'Indigestion', 'Muscle wasting', 'Patches in throat', 'High fever', 'Extra marital contacts', 'Fatigue', 'Weight loss', 'Restlessness', 'Lethargy', 'Irregular sugar level', 'Blurred and distorted vision', 'Obesity', 'Excessive hunger', 'Increased appetite', 'Polyuria', 'Sunken eyes', 'Dehydration', 'Diarrhoea', 'Breathlessness', 'Family history', 'Mucoid sputum', 'Headache', 'Dizziness', 'Loss of balance', 'Lack of concentration', 'Stiff neck', 'Depression', 'Irritability', 'Visual disturbances', 'Back pain', 'Weakness in limbs', 'Neck pain', 'Weakness of one body side', 'Altered sensorium', 'Dark urine', 'Sweating', 'Muscle pain', 'Mild fever', 'Swelled lymph nodes', 'Malaise', 'Red spots over body', 'Joint pain', 'Pain behind the eyes', 'Constipation', 'Toxic look (typhos)', 'Belly pain', 'Yellow urine', 'Receiving blood transfusion', 'Receiving unsterile injections', 'Coma', 'Stomach bleeding', 'Acute liver failure', 'Swelling of stomach', 'Distention of abdomen', 'History of alcohol consumption', 'Fluid overload', 'Phlegm', 'Blood in sputum', 'Throat irritation', 'Redness of eyes', 'Sinus pressure', 'Runny nose', 'Congestion', 'Loss of smell', 'Fast heart rate', 'Rusty sputum', 'Pain during bowel movements', 'Pain in anal region', 'Bloody stool', 'Irritation in anus', 'Cramps', 'Bruising', 'Swollen legs', 'Swollen blood vessels', 'Prominent veins on calf', 'Weight gain', 'Cold hands and feets', 'Mood swings', 'Puffy face and eyes', 'Enlarged thyroid', 'Brittle nails', 'Swollen extremeties', 'Abnormal menstruation', 'Muscle weakness', 'Anxiety', 'Slurred speech', 'Palpitations', 'Drying and tingling lips', 'Knee pain', 'Hip joint pain', 'Swelling joints', 'Painful walking', 'Movement stiffness', 'Spinning movements', 'Unsteadiness', 'Pus filled pimples', 'Blackheads', 'Scurring', 'Bladder discomfort', 'Foul smell ofurine', 'Continuous feel of urine', 'Skin peeling', 'Silver like dusting', 'Small dents in nails', 'Inflammatory nails', 'Blister', 'Red sore around nose', 'Yellow crust ooze']

    var dataList = document.getElementById("tag-list");
    symptoms.forEach(function(symptom) {
        var option = document.createElement("option");
        option.value = symptom;
        dataList.appendChild(option);
    });
});

// Handling tag input and display
document.getElementById("tag-input").addEventListener("input", function (e) {
    var selectedTag = e.target.value;
    var tagsContainer = document.getElementById("tags-container");
    var tagList = document.getElementById("tag-list");
    if (selectedTag) {
        var tag = document.createElement("div");
        tag.className = "tag bg-blue-500 text-white rounded-full px-3 py-1 m-1 flex items-center shadow-md cursor-pointer transition-colors duration-200 ease-in-out hover:bg-blue-600";

        var tagText = document.createElement("span");
        tagText.innerText = selectedTag;

        var removeButton = document.createElement("span");
        removeButton.innerHTML = "&times;";
        removeButton.className = "ml-2 font-bold";
        removeButton.onclick = function () {
            tagsContainer.removeChild(tag);
            var option = document.createElement("option");
            option.value = selectedTag;
            tagList.appendChild(option);
        };

        tag.appendChild(tagText);
        tag.appendChild(removeButton);
        tagsContainer.appendChild(tag);
        e.target.value = "";

        var options = tagList.options;
        for (var i = 0; i < options.length; i++) {
            if (options[i].value === selectedTag) {
                tagList.removeChild(options[i]);
                break;
            }
        }
    }
});
document.getElementById("tags-form").addEventListener("submit", function(e) {
    e.preventDefault(); 
    window.location.href = "Results.html"; 
});