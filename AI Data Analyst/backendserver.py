
@api_router.post(\"/upload\")
async def upload_dataset(file: UploadFile = File(...)):
    \"\"\"Upload a CSV or Excel file and return preview + statistics\"\"\"
    try:
        contents = await file.read()
        
        # Determine file type and read accordingly
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail=\"Only CSV and Excel files are supported\")
        
        # Store in memory
        current_dataset[\"df\"] = df
        current_dataset[\"filename\"] = file.filename
        current_dataset[\"columns\"] = df.columns.tolist()
        current_dataset[\"shape\"] = {\"rows\": len(df), \"columns\": len(df.columns)}
        
        # Generate basic statistics
        stats = {}
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            stats_df = df[numeric_cols].describe()
            stats = stats_df.to_dict()
        
        current_dataset[\"stats\"] = stats
        
        # Get preview (first 5 rows)
        preview = df.head(5).to_dict('records')
        
        return JSONResponse(content={
            \"filename\": file.filename,
            \"shape\": current_dataset[\"shape\"],
            \"columns\": current_dataset[\"columns\"],
            \"preview\": preview,
            \"stats\": stats,
            \"message\": \"Dataset uploaded successfully\"
        })
    
    except Exception as e:
        logging.error(f\"Error uploading file: {str(e)}\")
        raise HTTPException(status_code=500, detail=str(e))" --new-str "@api_router.post(\"/upload\")
async def upload_dataset(file: UploadFile = File(...)):
    \"\"\"Upload a CSV or Excel file and return preview + statistics\"\"\"
    try:
        # Validate file type first
        if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail=\"Only CSV and Excel files are supported\")
        
        contents = await file.read()
        
        # Determine file type and read accordingly
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        
        # Store in memory
        current_dataset[\"df\"] = df
        current_dataset[\"filename\"] = file.filename
        current_dataset[\"columns\"] = df.columns.tolist()
        current_dataset[\"shape\"] = {\"rows\": len(df), \"columns\": len(df.columns)}
        
        # Generate basic statistics
        stats = {}
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            stats_df = df[numeric_cols].describe()
            stats = stats_df.to_dict()
        
        current_dataset[\"stats\"] = stats
        
        # Get preview (first 5 rows)
        preview = df.head(5).to_dict('records')
        
        return JSONResponse(content={
            \"filename\": file.filename,
            \"shape\": current_dataset[\"shape\"],
            \"columns\": current_dataset[\"columns\"],
            \"preview\": preview,
            \"stats\": stats,
            \"message\": \"Dataset uploaded successfully\"
        })
    
    except HTTPException:
        raise
    except pd.errors.ParserError as e:
        logging.error(f\"Invalid file format: {str(e)}\")
        raise HTTPException(status_code=400, detail=\"Invalid file format. Please upload a valid CSV or Excel file.\")
    except Exception as e:
        logging.error(f\"Error uploading file: {str(e)}\")
        raise HTTPException(status_code=400, detail=f\"Failed to process file: {str(e)}\")"
