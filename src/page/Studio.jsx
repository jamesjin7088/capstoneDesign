import "./Studio.css";
import ImageUpload from "../components/ImageUpload";

const Studio = () => {
  return (
    <div className="Studio">
      <div>
        <section className="section1">
          <div className="section1-1">
            <h2>Upload Image</h2>
            <span>Step 1 of 4</span>
          </div>
          <div className="section1-2"></div>
        </section>

        <ImageUpload />
      </div>
    </div>
  );
};

export default Studio;
