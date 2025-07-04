# Deploy Honor Society API to Render

## 🚀 **Render Deployment Guide**

### **Prerequisites**
- GitHub account with your code pushed
- Render account (free tier available)
- Your Honor Society API codebase

---

## **Step 1: Prepare Your Repository**

### **1.1 Push to GitHub**
Make sure your code is pushed to GitHub:
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### **1.2 Verify Required Files**
✅ Your project already has these files:
- `requirements.txt` - ✅ Already configured
- `Procfile` - ✅ Already configured  
- `settings.py` - ✅ Production-ready
- `.env.example` - ✅ Template available

---

## **Step 2: Create PostgreSQL Database on Render**

### **2.1 Create Database**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New"** → **"PostgreSQL"**
3. Fill in the details:
   - **Name**: `honor-society-db`
   - **Database**: `honor_society_db`
   - **User**: `honor_society_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)

### **2.2 Get Database Connection Info**
After creation, you'll get:
- **Database URL**: `postgresql://user:password@host:port/dbname`
- **Host**: `hostname`
- **Port**: `5432`
- **Database**: `dbname`
- **Username**: `username`  
- **Password**: `password`

---

## **Step 3: Create Web Service on Render**

### **3.1 Create Web Service**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Fill in the details:
   - **Name**: `honor-society-api`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn honor_system.wsgi:application`

### **3.2 Configure Environment Variables**
Add these environment variables in Render:

```env
# Security
SECRET_KEY=your-super-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

# Database (from Step 2)
DB_NAME=honor_society_db
DB_USER=honor_society_user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-app-name.onrender.com

# Don't use SQLite in production
USE_SQLITE=False
```

---

## **Step 4: Deploy**

### **4.1 Trigger Deployment**
1. Click **"Create Web Service"**
2. Render will automatically:
   - Pull your code from GitHub
   - Install dependencies
   - Run migrations (via `release` command in Procfile)
   - Start your application

### **4.2 Monitor Deployment**
- Check the **"Logs"** tab for deployment progress
- Look for successful migration messages
- Verify the service starts without errors

---

## **Step 5: Post-Deployment Setup**

### **5.1 Create Superuser**
Connect to your Render service via SSH or use the web shell:
```bash
python manage.py createsuperuser
```

### **5.2 Test Your API**
Your API will be available at:
- **Base URL**: `https://your-app-name.onrender.com`
- **Admin**: `https://your-app-name.onrender.com/admin/`
- **API Docs**: `https://your-app-name.onrender.com/api/`

### **5.3 Test Key Endpoints**
```bash
# Test health
GET https://your-app-name.onrender.com/api/campuses/

# Test authentication
POST https://your-app-name.onrender.com/api/token/
{
  "username": "your-username",
  "password": "your-password"
}
```

---

## **Step 6: Custom Domain (Optional)**

### **6.1 Add Custom Domain**
1. Go to your web service settings
2. Add your domain in **"Custom Domains"**
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`

---

## **Step 7: Monitoring & Maintenance**

### **7.1 Set Up Monitoring**
- Enable **"Auto Deploy"** for automatic updates
- Monitor logs regularly
- Set up health checks

### **7.2 Regular Maintenance**
- Update dependencies regularly
- Monitor database performance
- Backup your database

---

## **🔧 Troubleshooting**

### **Common Issues**

**1. Database Connection Error**
- Verify database credentials
- Check if database service is running
- Ensure database and web service are in same region

**2. Static Files Not Loading**
- Your `whitenoise` configuration should handle this
- Check `STATIC_ROOT` and `STATICFILES_STORAGE` settings

**3. CORS Issues**
- Update `CORS_ALLOWED_ORIGINS` with your frontend domain
- Ensure frontend URL matches exactly (https/http)

**4. Migration Errors**
- Check if `release` command in Procfile is correct
- Run migrations manually via Render shell if needed

---

## **🎯 Final Checklist**

Before going live:
- [ ] Database is created and accessible
- [ ] Environment variables are set correctly
- [ ] Superuser is created
- [ ] API endpoints are working
- [ ] CORS is configured for your frontend
- [ ] SSL/HTTPS is working
- [ ] Monitoring is set up

---

## **📞 Support**

If you encounter issues:
1. Check Render logs first
2. Verify environment variables
3. Test database connectivity
4. Contact Render support if needed

Your Honor Society API is now live and ready for production use! 🎉
